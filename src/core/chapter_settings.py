class ChapterSettings:
    DEFAULT_LIST_MARKERS = ['-', '+', '*']

    @classmethod
    def get_file_settings(cls, config, filename: str) -> dict:
        settings = getattr(config, 'settings', {}) or {}
        chapter_settings = settings.get('chapter_settings', {}) or {}
        file_settings = chapter_settings.get(filename, {}) or {}
        if not isinstance(file_settings, dict):
            return {}
        return file_settings

    @classmethod
    def get_list_markers_by_level(cls, config, filename: str) -> list[str]:
        file_settings = cls.get_file_settings(config, filename)
        raw_markers = file_settings.get('list_markers_by_level', cls.DEFAULT_LIST_MARKERS)
        return cls.normalize_list_markers(raw_markers)

    @classmethod
    def get_list_marker(cls, config, filename: str, level: int) -> str:
        markers = cls.get_list_markers_by_level(config, filename)
        safe_level = max(1, int(level))
        if safe_level <= len(markers):
            return markers[safe_level - 1]
        return markers[-1]

    @classmethod
    def normalize_list_markers(cls, raw_markers) -> list[str]:
        defaults = list(cls.DEFAULT_LIST_MARKERS)
        if not isinstance(raw_markers, list):
            return defaults

        normalized = []
        for index, default_value in enumerate(defaults):
            raw_value = raw_markers[index] if index < len(raw_markers) else default_value
            marker = str(raw_value).strip() if raw_value is not None else ''
            normalized.append(marker or default_value)

        for raw_value in raw_markers[len(defaults):]:
            marker = str(raw_value).strip() if raw_value is not None else ''
            normalized.append(marker or normalized[-1])

        return normalized
