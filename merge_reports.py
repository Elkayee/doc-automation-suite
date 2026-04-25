import sys
from docx import Document

def merge_docx_files(file_list, output_filename):
    """
    Nối danh sách các file docx thành một file duy nhất.
    Giữ nguyên các paragraph, styles và định dạng cơ bản.
    """
    if not file_list:
        print("No files to merge.")
        return

    # Start with the first document
    merged_document = Document(file_list[0])

    for i in range(1, len(file_list)):
        # Add a page break before each new file
        merged_document.add_page_break()

        sub_doc = Document(file_list[i])

        # Copy elements from sub_doc to merged_document
        for element in sub_doc.element.body:
            # We skip the SectPr (Section Properties) which usually contains page setup
            # that might conflict if not handled carefully, but for simple merging
            # appending to body is usually sufficient.
            if element.tag.endswith('sectPr'):
                continue
            merged_document.element.body.append(element)

    merged_document.save(output_filename)
    print(f"Successfully created: {output_filename}")

if __name__ == "__main__":
    # Logical order for the super report
    files = [
        "Bao_Cao_Chung_Phan1_KhaoSat.docx",
        "Bao_Cao_Chung_Phan2_ThietKe.docx",
        "Bao_Cao_NMCNPM_Cafe_Final_Integrated.docx", # Contains P3 & P4 content
        "Bao_Cao_Ca_Nhan_UC04_Final_Full.docx"       # Detailed individual result
    ]

    merge_docx_files(files, "BAO_CAO_CUOI_KY_NMCNPM_QUAN_CAFE.docx")
