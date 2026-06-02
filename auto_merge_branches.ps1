<#
.SYNOPSIS
    Automatically merges all eligible remote branches into the current base branch.

.DESCRIPTION
    This script:
      1. Validates the working directory is clean and you are on master/main.
      2. Updates the base branch from origin.
      3. Fetches and prunes all remote branches.
      4. For each eligible remote branch, performs a dry-test merge (--no-commit --no-ff).
      5. If mergeable  -> commits the merge, deletes remote & local tracking branch.
      6. If conflict   -> aborts, reports it. If -DeleteConflicted is set, deletes the branch. Otherwise SKIPS it.
      7. If up-to-date -> skips silently (already merged).
      8. Pushes accumulated merges to origin.
      9. Prints a structured summary table at the end.

.PARAMETER DryRun
    Simulate all operations without actually making any git changes.

.PARAMETER SkipPush
    Merge locally but do not push to origin at the end.

.PARAMETER DeleteConflicted
    If a conflict is detected, delete the remote and local branch instead of skipping it.

.PARAMETER LogFile
    Optional path to write a log file. Defaults to no log file.

.EXAMPLE
    .\auto_merge_branches.ps1
    .\auto_merge_branches.ps1 -DryRun
    .\auto_merge_branches.ps1 -SkipPush -LogFile "merge_log.txt"
#>
param (
    [switch]$DryRun,
    [switch]$SkipPush,
    [switch]$DeleteConflicted,
    [string]$LogFile = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Logging helper ─────────────────────────────────────────────────────────────
function Write-Log {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $Message"
    Write-Host $line -ForegroundColor $Color
    if ($LogFile -ne "") {
        Add-Content -Path $LogFile -Value $line
    }
}

# ── Git helper: run git, capture output, check exit code ──────────────────────
function Invoke-Git {
    param([string[]]$Arguments)
    $output = (& git @Arguments 2>$null) | Out-String
    if ($LASTEXITCODE -ne 0) {
        # Return output even on failure; caller decides how to handle
        return [PSCustomObject]@{ Success = $false; Output = $output.Trim() }
    }
    return [PSCustomObject]@{ Success = $true; Output = $output.Trim() }
}

# ── Banner ─────────────────────────────────────────────────────────────────────
Write-Log "================================================" "Cyan"
Write-Log "       SlotMaster - Auto-Merge Script           " "Cyan"
Write-Log "================================================" "Cyan"
if ($DryRun) {
    Write-Log ">>> DRY RUN MODE - No changes will be made <<<" "Yellow"
}

# ── Tracking collections for summary ──────────────────────────────────────────
$mergedBranches   = [System.Collections.Generic.List[string]]::new()
$conflictBranches = [System.Collections.Generic.List[string]]::new()
$skippedBranches  = [System.Collections.Generic.List[string]]::new()

# ── Step 1: Ensure working directory is clean ─────────────────────────────────
Write-Log ""
Write-Log "[1/5] Checking working directory..." "Gray"
$statusResult = Invoke-Git @("status", "--porcelain")
if ($statusResult.Output -ne "") {
    Write-Log "ERROR: Working directory is not clean. Commit or stash your changes first." "Red"
    Write-Log "       Uncommitted changes detected:" "Red"
    Write-Log "       $($statusResult.Output)" "Red"
    exit 1
}
Write-Log "      Working directory is clean." "Green"

# ── Step 2: Ensure we are on master or main ───────────────────────────────────
Write-Log ""
Write-Log "[2/5] Checking current branch..." "Gray"
$currentBranch = (Invoke-Git @("branch", "--show-current")).Output
if ($currentBranch -notmatch '^(master|main)$') {
    Write-Log "ERROR: You are on branch '$currentBranch'. Please checkout 'master' or 'main' first." "Red"
    exit 1
}
Write-Log "      Current branch: $currentBranch" "Green"

# ── Step 3: Update base branch ────────────────────────────────────────────────
Write-Log ""
Write-Log "[3/5] Updating base branch '$currentBranch' from origin..." "Gray"
if (-not $DryRun) {
    $fetchBase = Invoke-Git @("fetch", "origin", $currentBranch)
    if (-not $fetchBase.Success) {
        Write-Log "WARNING: Could not fetch origin/$currentBranch. Continuing with local state." "Yellow"
        Write-Log "         $($fetchBase.Output)" "Yellow"
    }
    $pullResult = Invoke-Git @("pull", "origin", $currentBranch)
    if (-not $pullResult.Success) {
        Write-Log "ERROR: Failed to pull origin/$currentBranch." "Red"
        Write-Log "       $($pullResult.Output)" "Red"
        exit 1
    }
    Write-Log "      Base branch updated." "Green"
} else {
    Write-Log "      [DRY RUN] Would fetch and pull origin/$currentBranch." "Yellow"
}

# ── Step 4: Fetch and prune all remote branches ───────────────────────────────
Write-Log ""
Write-Log "[4/5] Fetching and pruning all remote branches..." "Gray"
if (-not $DryRun) {
    $fetchAll = Invoke-Git @("fetch", "--all", "--prune")
    if (-not $fetchAll.Success) {
        Write-Log "WARNING: fetch --all --prune returned non-zero. Some branches may be stale." "Yellow"
    }
    Write-Log "      Fetch complete." "Green"
} else {
    Write-Log "      [DRY RUN] Would run: git fetch --all --prune" "Yellow"
}

# ── Step 5: Collect eligible remote branches ──────────────────────────────────
Write-Log ""
Write-Log "[5/5] Collecting eligible remote branches..." "Gray"

# Branches to never touch (pattern match)
$excludedPattern = '^origin/(HEAD|master|main|develop|release/.+|staging)(\s|$)'

$allRemote = (& git branch -r) -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$remoteBranches = $allRemote | Where-Object {
    ($_ -match '^origin/') -and ($_ -notmatch $excludedPattern) -and ($_ -notmatch '\s->\s')
}

if (-not $remoteBranches -or $remoteBranches.Count -eq 0) {
    Write-Log "      No eligible remote branches found to process." "Yellow"
} else {
    Write-Log "      Found $($remoteBranches.Count) branch(es) to evaluate." "Green"
}

# ── Main merge loop ───────────────────────────────────────────────────────────
Write-Log ""
Write-Log "── Processing Branches ──────────────────────────────────────────────" "Cyan"

foreach ($branch in $remoteBranches) {
    $localBranchName = $branch -replace '^origin/', ''

    Write-Log ""
    Write-Log "  Branch: $branch" "White"

    # ── Test-merge (--no-commit --no-ff) ──────────────────────────────────────
    if (-not $DryRun) {
        $testMerge = Invoke-Git @("merge", "--no-commit", "--no-ff", $branch)
        $mergeOutput = $testMerge.Output

        # ── Case A: Already up to date ────────────────────────────────────────
        if ($mergeOutput -match "Already up to date" -or $mergeOutput -match "up-to-date") {
            Write-Log "    -> Already up to date. Skipping." "DarkGray"
            $skippedBranches.Add($localBranchName)
            # No merge state to abort
            continue
        }

        # ── Case B: Conflict ──────────────────────────────────────────────────
        if ($mergeOutput -match "CONFLICT" -or $mergeOutput -match "Automatic merge failed") {
            Invoke-Git @("merge", "--abort") | Out-Null
            if ($DeleteConflicted) {
                Write-Log "    -> CONFLICT detected. Deleting conflicted branch..." "Red"
                
                # Delete remote branch
                $delRemote = Invoke-Git @("push", "origin", "--delete", $localBranchName)
                if ($delRemote.Success) {
                    Write-Log "    -> Remote branch 'origin/$localBranchName' deleted." "DarkGray"
                } else {
                    Write-Log "    -> WARNING: Could not delete remote branch 'origin/$localBranchName'." "Yellow"
                    Write-Log "       $($delRemote.Output)" "Yellow"
                }

                # Delete local tracking branch if it exists
                $localExists = ((& git branch --list $localBranchName) -join '').Trim()
                if ($localExists -ne "") {
                    $delLocal = Invoke-Git @("branch", "-D", $localBranchName)
                    if ($delLocal.Success) {
                        Write-Log "    -> Local branch '$localBranchName' deleted." "DarkGray"
                    } else {
                        Write-Log "    -> WARNING: Could not delete local branch '$localBranchName'." "Yellow"
                    }
                }
            } else {
                Write-Log "    -> CONFLICT detected. Aborting test merge. Branch will NOT be deleted." "Red"
            }
            $conflictBranches.Add($localBranchName)
            continue
        }

        # ── Case C: Mergeable ─────────────────────────────────────────────────
        Write-Log "    -> Mergeable. Committing..." "Green"
        $commitResult = Invoke-Git @("commit", "-m", "chore: Auto-merge branch $localBranchName into $currentBranch", "--no-edit")
        if (-not $commitResult.Success) {
            Write-Log "    -> Commit failed (possibly nothing to commit). Aborting." "Yellow"
            Invoke-Git @("merge", "--abort") | Out-Null
            $skippedBranches.Add($localBranchName)
            continue
        }
        Write-Log "    -> Merge committed." "Green"

        # Delete remote branch
        $delRemote = Invoke-Git @("push", "origin", "--delete", $localBranchName)
        if ($delRemote.Success) {
            Write-Log "    -> Remote branch 'origin/$localBranchName' deleted." "DarkGray"
        } else {
            Write-Log "    -> WARNING: Could not delete remote branch 'origin/$localBranchName'." "Yellow"
            Write-Log "       $($delRemote.Output)" "Yellow"
        }

        # Delete local tracking branch if it exists
        $localExists = ((& git branch --list $localBranchName) -join '').Trim()
        if ($localExists -ne "") {
            $delLocal = Invoke-Git @("branch", "-d", $localBranchName)
            if ($delLocal.Success) {
                Write-Log "    -> Local branch '$localBranchName' deleted." "DarkGray"
            } else {
                Write-Log "    -> WARNING: Could not delete local branch '$localBranchName' (may have unmerged commits)." "Yellow"
            }
        }

        $mergedBranches.Add($localBranchName)

    } else {
        # ── DRY RUN simulation ────────────────────────────────────────────────
        # Do a real test-merge to see what WOULD happen, then abort
        $testMerge = Invoke-Git @("merge", "--no-commit", "--no-ff", $branch)
        $mergeOutput = $testMerge.Output

        if ($mergeOutput -match "Already up to date" -or $mergeOutput -match "up-to-date") {
            Write-Log "    -> [DRY RUN] Already up to date. Would skip." "DarkGray"
            $skippedBranches.Add($localBranchName)
        } elseif ($mergeOutput -match "CONFLICT" -or $mergeOutput -match "Automatic merge failed") {
            if ($DeleteConflicted) {
                Write-Log "    -> [DRY RUN] CONFLICT detected. Would delete remote & local branch." "Red"
            } else {
                Write-Log "    -> [DRY RUN] CONFLICT detected. Would skip (branch NOT deleted)." "Red"
            }
            Invoke-Git @("merge", "--abort") | Out-Null
            $conflictBranches.Add($localBranchName)
        } else {
            Write-Log "    -> [DRY RUN] Would merge, commit, delete remote & local branch." "Yellow"
            Invoke-Git @("merge", "--abort") | Out-Null
            $mergedBranches.Add($localBranchName)
        }
    }
}

# ── Push merged changes to origin ─────────────────────────────────────────────
Write-Log ""
Write-Log "── Post-Processing ─────────────────────────────────────────────────" "Cyan"
if ($mergedBranches.Count -gt 0 -and -not $DryRun -and -not $SkipPush) {
    Write-Log "  Pushing $($mergedBranches.Count) merge(s) to origin/$currentBranch..." "Cyan"
    $pushResult = Invoke-Git @("push", "origin", $currentBranch)
    if ($pushResult.Success) {
        Write-Log "  Push successful." "Green"
    } else {
        Write-Log "  ERROR: Push to origin/$currentBranch FAILED." "Red"
        Write-Log "         $($pushResult.Output)" "Red"
        Write-Log "  You may need to push manually with: git push origin $currentBranch" "Yellow"
    }
} elseif ($DryRun) {
    Write-Log "  [DRY RUN] Would push to origin/$currentBranch." "Yellow"
} elseif ($SkipPush) {
    Write-Log "  Skipping push (--SkipPush flag set). Run manually: git push origin $currentBranch" "Yellow"
} else {
    Write-Log "  No merges performed. Nothing to push." "Gray"
}

# ── Summary Table ──────────────────────────────────────────────────────────────
Write-Log ""
Write-Log "════════════════════════════════════════════" "Cyan"
Write-Log "              SUMMARY REPORT                " "Cyan"
Write-Log "════════════════════════════════════════════" "Cyan"
Write-Log ("  Merged    : {0,3}  branch(es)" -f $mergedBranches.Count)   "Green"
Write-Log ("  Conflicts : {0,3}  branch(es)" -f $conflictBranches.Count) "Red"
Write-Log ("  Skipped   : {0,3}  branch(es)" -f $skippedBranches.Count)  "Gray"
Write-Log "────────────────────────────────────────────" "Cyan"

if ($mergedBranches.Count -gt 0) {
    Write-Log "  Merged branches:" "Green"
    foreach ($b in $mergedBranches) { Write-Log "    + $b" "Green" }
}
if ($conflictBranches.Count -gt 0) {
    if ($DeleteConflicted) {
        Write-Log "  Conflicting branches (deleted):" "Red"
    } else {
        Write-Log "  Conflicting branches (manual resolution needed):" "Red"
    }
    foreach ($b in $conflictBranches) { Write-Log "    ! $b" "Red" }
}
if ($skippedBranches.Count -gt 0) {
    Write-Log "  Skipped branches (already up to date):" "Gray"
    foreach ($b in $skippedBranches) { Write-Log "    ~ $b" "Gray" }
}

Write-Log "════════════════════════════════════════════" "Cyan"
Write-Log "  Script completed successfully." "Green"
Write-Log "════════════════════════════════════════════" "Cyan"
