# Đối chiếu pháp lý: Nghị định 30/2020/NĐ-CP

Ngày rà soát: 2026-10-09. Người dùng xác nhận đối chiếu với Nghị định 30/2020/NĐ-CP và văn bản hành
chính. Source baseline: `7b4b3d6e14c20a352d1a4c8e35868329cf95ed76`, phiên bản 0.2.1.

**Kết luận: app chưa đáp ứng đầy đủ thể thức và kỹ thuật tạo lập văn bản hành chính theo Nghị
định 30.** App hiện tạo báo cáo/biên bản từ khung chung. A4, lề mặc định, lời văn và màu chữ đen đạt
trên mẫu đã xuất; đầu/cuối văn bản hành chính, số trang, font/cỡ tiêu đề và kiểm tra tuân thủ trước
khi xuất còn thiếu hoặc sai. Cả ba mẫu thử đều được xuất `final` với `success=true`, `warnings=[]`,
dù thiếu thành phần hành chính; mẫu cố ý sai font/lề/ giãn dòng cũng được chấp nhận. Chi tiết và
bằng chứng nằm ở phần kết quả app cuối tài liệu.

Phạm vi đã kiểm tra: nguồn pháp lý chính thức, mã nguồn/mẫu, GUI source thật, DOCX/PDF thật từ bản
sao cô lập. Chưa kiểm tra EXE đóng gói trong phiên này. Chỉ bổ sung tài liệu rà soát; chưa sửa chức
năng hoặc mẫu của app.

## Kết luận pháp lý cần giữ khi đánh giá

- Cơ sở dữ liệu pháp luật của Bộ Nội vụ hiện ghi Nghị định 30/2020/NĐ-CP là **còn hiệu lực**, có
  hiệu lực từ 05/03/2020. Lịch sử hiệu lực ghi nhận ngày ban hành và ngày có hiệu lực đều là
  05/03/2020. Nghị định 110/2004/NĐ-CP và Nghị định 09/2010/NĐ-CP hết hiệu lực từ thời điểm Nghị
  định 30 có hiệu lực.
- Điều 2 áp dụng trực tiếp cho cơ quan, tổ chức nhà nước và doanh nghiệp nhà nước. Tổ chức chính
  trị, tổ chức chính trị - xã hội, tổ chức xã hội, tổ chức xã hội - nghề nghiệp căn cứ Nghị định và
  quy định liên quan để áp dụng phù hợp. Một bài tập hoặc báo cáo học thuật cá nhân không tự động
  trở thành “văn bản hành chính” chỉ vì dùng đúng mẫu; trường, cơ quan hoặc đơn vị có thể đặt quy
  định riêng hoặc chủ động chọn Nghị định làm chuẩn.
- Nghị định điều chỉnh cả soạn thảo, ký ban hành, quản lý văn bản, lập hồ sơ - nộp lưu và quản lý
  con dấu/thiết bị lưu khóa bí mật (Điều 1). Vì vậy, kiểm tra bố cục DOCX chỉ bao phủ một phần yêu
  cầu; nó không chứng minh app có quy trình phát hành, ký số, đăng ký, thu hồi, theo dõi hay lưu trữ
  văn bản.

## Nguồn chính thức đã sử dụng

1. [Cổng thông tin điện tử Chính phủ: trang Nghị định 30/2020/NĐ-CP](https://vanban.chinhphu.vn/default.aspx?docid=199378&pageid=27160),
   ghi số hiệu, ngày ban hành, cơ quan ban hành và bản PDF đã ký.
2. [Bản PDF đã ký trên datafiles.chinhphu.vn](https://datafiles.chinhphu.vn/cpp/files/vbpq/2020/03/30.signed.pdf),
   gồm toàn văn và Phụ lục I-VI.
3. [CSDL pháp luật của Bộ Nội vụ - toàn văn](https://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=141142&dvid=320),
   gồm Điều 1-38, trạng thái hiệu lực và các tệp Phụ lục.
4. [CSDL pháp luật của Bộ Nội vụ - lịch sử hiệu lực](https://vbpl.vn/bonoivu/Pages/vbpq-lichsu.aspx?ItemID=141142&Keyword=&dvid=320),
   dùng để kiểm tra trạng thái tại ngày rà soát.
5. [Công báo điện tử Chính phủ](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-30-2020-nd-cp-30858/30246.htm),
   bản Công báo 283 + 284 và liên kết tải PDF/DOC chính thức.
6. [Bản PDF trên cổng Bộ Tư pháp](https://thads.moj.gov.vn/tphochiminh/noidung/tintuc/Lists/ThongTinKhac/Attachments/52/nghi-dinh-30-2020-nd-cp-ve-cong-tac-van-thu.pdf),
   bản sao chính thức dùng để tra nhanh nội dung các Phụ lục khi bản PDF Cổng Chính phủ là bản quét.

Khi có khác biệt giữa bài hướng dẫn, mẫu của trường/cơ quan và văn bản pháp luật, dùng toàn văn Nghị
định và Phụ lục làm nguồn pháp lý; mẫu riêng chỉ là yêu cầu bổ sung trong phạm vi đơn vị áp dụng.

## Checklist bắt buộc cho văn bản hành chính

### 1. Phạm vi, loại văn bản và cấu trúc (Điều 2, Điều 7-9)

- [ ] Phân loại đúng ngữ cảnh: văn bản hành chính hình thành trong hoạt động chỉ đạo, điều hành,
      giải quyết công việc (Điều 3 khoản 3); văn bản chuyên ngành theo quy định của người đứng đầu
      ngành; văn bản quy phạm pháp luật theo luật riêng.
- [ ] Nếu app tuyên bố hỗ trợ văn bản hành chính, phải nhận diện được các loại tại Điều 7: nghị
      quyết (cá biệt), quyết định (cá biệt), chỉ thị, quy chế, quy định, thông cáo, thông báo, hướng
      dẫn, chương trình, kế hoạch, phương án, đề án, dự án, báo cáo, biên bản, tờ trình, hợp đồng,
      công văn, công điện, bản ghi nhớ, bản thỏa thuận, giấy ủy quyền, giấy mời, giấy giới thiệu,
      giấy nghỉ phép, phiếu gửi, phiếu chuyển, phiếu báo và thư công. Không cần suy ra rằng app phải
      cung cấp mọi loại nếu sản phẩm đã công bố phạm vi hẹp; khi đó phạm vi phải được ghi rõ.
- [ ] Thành phần chính của văn bản hành chính theo Điều 8 khoản 2: Quốc hiệu và Tiêu ngữ; tên cơ
      quan/tổ chức ban hành; số, ký hiệu; địa danh và thời gian ban hành; tên loại và trích yếu; nội
      dung; chức vụ, họ tên và chữ ký người có thẩm quyền; dấu/chữ ký số của cơ quan, tổ chức; nơi
      nhận.
- [ ] Thành phần bổ sung khi trường hợp cụ thể cần có: phụ lục; dấu mật/mức độ khẩn/chỉ dẫn phạm vi
      lưu hành; ký hiệu người soạn thảo và số lượng bản phát hành; địa chỉ, email, website, điện
      thoại, fax (Điều 8 khoản 3).
- [ ] Thể thức, kỹ thuật, viết hoa và chữ viết tắt phải quy chiếu lần lượt Phụ lục I, II và III
      (Điều 8 khoản 4, Điều 9). Mẫu Phụ lục III là mẫu trình bày và bảng chữ viết tắt, không phải
      bằng chứng rằng mọi báo cáo học thuật phải dùng toàn bộ thể thức công vụ.

### 2. Khổ giấy, lề, phông, đoạn và số trang (Phụ lục I, Phần I, Mục I và Mục II)

- [ ] Khổ A4, 210 x 297 mm.
- [ ] Trình bày theo chiều dài khổ A4; chỉ dùng chiều rộng khi nội dung có bảng/biểu không tách
      thành phụ lục riêng.
- [ ] Lề trên và dưới 20-25 mm; lề trái 30-35 mm; lề phải 15-20 mm.
- [ ] Phông tiếng Việt Times New Roman, mã Unicode theo TCVN 6909:2001, màu đen. Việc kiểm tra phải
      bao gồm chữ trong style kế thừa, tiêu đề, chú thích, bảng, liên kết, header/footer và field;
      kiểm tra một vài heading là chưa đủ.
- [ ] Cỡ và kiểu chữ theo từng thành phần thể thức. Phần lời văn: chữ in thường, căn đều hai lề,
      kiểu đứng, cỡ 13-14; đầu đoạn lùi 1 cm hoặc 1,27 cm; khoảng cách đoạn tối thiểu 6 pt; khoảng
      cách dòng tối thiểu single và tối đa 1,5 lines.
- [ ] Số trang dùng chữ số Ả Rập, cỡ 13-14, kiểu đứng, canh giữa theo chiều ngang trong lề trên;
      không hiển thị số trang thứ nhất theo quy tắc Phụ lục I.

### 3. Đầu trang, định danh và nội dung thể thức (Phụ lục I, Phần I, Mục II-IV)

- [ ] Quốc hiệu “CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM”: in hoa, cỡ 12-13, đứng, đậm, phía trên cùng
      bên phải trang đầu.
- [ ] Tiêu ngữ “Độc lập - Tự do - Hạnh phúc”: chữ thường theo quy tắc viết hoa chữ cái đầu, cỡ
      13-14, đứng, đậm, căn giữa dưới Quốc hiệu, có đường kẻ ngang phía dưới.
- [ ] Phụ lục I quy định thành phần **Quốc hiệu và Tiêu ngữ** bằng chữ; không liệt kê hình ảnh quốc
      huy/logo là một thành phần chính bắt buộc. Logo hoặc huy hiệu của đơn vị chỉ nên đưa vào khi
      có mẫu/ủy quyền riêng, không biến thành kết luận pháp lý của Nghị định 30.
- [ ] Tên cơ quan/tổ chức là tên chính thức, đầy đủ, gồm cả cơ quan chủ quản trực tiếp nếu có; tên
      cơ quan ban hành in hoa, cỡ 12-13, đứng, đậm, căn giữa và có đường kẻ dưới.
- [ ] Số là số thứ tự văn bản đăng ký trong năm, bằng chữ số Ả Rập. Ký hiệu theo tên loại và cơ
      quan/chức danh; với công văn gồm cơ quan/chức danh và đơn vị soạn thảo hoặc lĩnh vực. Số và ký
      hiệu phải duy nhất trong năm giữa văn bản giấy và điện tử (Điều 15).
- [ ] Địa danh và ngày ban hành viết đầy đủ; ngày, tháng, năm bằng chữ số Ả Rập; ngày nhỏ hơn 10 và
      tháng 1 hoặc 2 thêm số 0 phía trước theo Phụ lục I.
- [ ] Văn bản có tên loại trình bày tên loại và trích yếu theo ô 5a; công văn không ghi tên loại,
      dùng trích yếu “V/v” theo ô 5b. Nội dung, căn cứ, điều/khoản/điểm và tiêu đề phải theo kiểu
      chữ, cỡ chữ, căn lề và quy tắc đánh số trong Phụ lục I.
- [ ] Chức vụ/quyền hạn và họ tên người có thẩm quyền ở ô 7; chức vụ chính thức, không tự thêm chức
      danh không có căn cứ. Trước họ tên không ghi học hàm, học vị hoặc danh hiệu danh dự, trừ
      trường hợp đơn vị vũ trang và tổ chức sự nghiệp giáo dục, y tế, khoa học do người đứng đầu
      ngành quy định.
- [ ] Nơi nhận ở ô 9; các mục tùy trường hợp (mật, khẩn, phạm vi lưu hành, người soạn thảo, số bản,
      thông tin liên hệ) phải ở đúng vị trí nếu được dùng. Phần “Nơi nhận” và dòng “Lưu” không được
      coi là văn bản điện tử đã phát hành nếu chưa có quy trình ký/phát hành tương ứng.

### 4. Viết hoa, viết tắt và mẫu (Phụ lục II-III)

- [ ] Dùng Phụ lục II cho viết hoa vì phép đặt câu; tên người, địa lý, dân tộc/tôn giáo; tên cơ
      quan/tổ chức; chức vụ, danh hiệu, huân chương/giải thưởng; tên văn bản; viện dẫn phần, chương,
      mục, điều, khoản, điểm và các trường hợp riêng. Không dùng một bộ quy tắc viết hoa tự phát cho
      mọi văn bản.
- [ ] Dùng đúng bảng Phụ lục III khi viết tắt tên loại. Các chữ viết tắt chính gồm: NQ, QĐ, CT, QC,
      QyĐ, TC, TB, HD, CTr, KH, PA, ĐA, DA, BC, BB, TTr, HĐ, CĐ, BGN, BTT, GUQ, GM, GGT, GNP, PG,
      PC, PB; bản sao gồm SY, TrS, SL.
- [ ] Nếu app dùng các mẫu 1.1-1.4 hoặc mẫu phụ lục, phải kiểm tra cả bản hiển thị và DOCX/PDF cuối
      cùng: vị trí ô, line, cỡ chữ, signature/seal, bảng và nơi nhận. Template chung không thay thế
      mẫu có thẩm quyền của trường/cơ quan.

### 5. Quy trình soạn thảo, duyệt, kiểm tra và ký (Điều 10-13)

- [ ] Người có thẩm quyền giao đơn vị/cá nhân chủ trì; người soạn thảo xác định tên loại, nội dung,
      độ mật, mức độ khẩn, thu thập/xử lý thông tin và soạn đúng thể thức. Với dự thảo điện tử, bản
      thảo và tài liệu kèm theo phải chuyển vào Hệ thống và cập nhật thông tin cần thiết (Điều 10).
- [ ] Bản thảo phải do người có thẩm quyền ký duyệt; bản thảo đã duyệt mà sửa phải trình lại người
      ký (Điều 11).
- [ ] Đơn vị soạn thảo chịu trách nhiệm về nội dung; người kiểm tra thể thức/kỹ thuật chịu trách
      nhiệm về thể thức/kỹ thuật trước khi ký (Điều 12). App có thể hỗ trợ cảnh báo, nhưng không
      thay thế trách nhiệm của người có thẩm quyền.
- [ ] Quyền ký, ký thay, thừa ủy quyền, thừa lệnh phải theo Điều 13 và quy chế của cơ quan; app
      không được tự suy đoán người ký từ tên tài khoản.
- [ ] Văn bản giấy ký bằng bút mực xanh, không dùng mực dễ phai (Điều 13 khoản 6). Đây là kiểm soát
      ngoài phần mềm.

## Văn bản điện tử và giới hạn của app tác giả

- Điều 5 chỉ công nhận văn bản điện tử có chữ ký số của người có thẩm quyền **và** chữ ký số của cơ
  quan/tổ chức theo pháp luật là có giá trị như bản gốc giấy. File DOCX/PDF do app xuất nhưng chưa
  qua ký số và phát hành không được tự gắn nhãn “bản gốc”, “đã ban hành” hoặc “đã hợp lệ”.
- Điều 14-19 yêu cầu luồng văn bản đi: cấp số/thời gian; đăng ký; nhân bản/đóng dấu hoặc ký số; phát
  hành và theo dõi; lưu bản gốc. Số và ngày của bản điện tử được cấp bằng chức năng của Hệ thống
  (Điều 15 khoản 3). Văn bản đi phải phát hành trong ngày ký, chậm nhất ngày làm việc tiếp theo; văn
  bản khẩn phát hành ngay (Điều 18).
- Bản gốc điện tử phải lưu trên Hệ thống của cơ quan. Chỉ Hệ thống đáp ứng Phụ lục VI và pháp luật
  liên quan mới được dùng để lưu bản gốc thay giấy; nếu chưa đáp ứng, Văn thư phải tạo bản chính
  giấy để lưu (Điều 19).
- Phụ lục VI áp dụng cho **Hệ thống quản lý tài liệu điện tử**, không phải mặc nhiên cho một trình
  soạn thảo cục bộ. Nếu app được quảng bá hoặc triển khai như Hệ thống phát hành/lưu văn bản,
  Control phải kiểm tra tối thiểu:
  - quản lý phân quyền, xác thực, độ tin cậy, toàn vẹn, khả năng kiểm chứng và nhật ký;
  - tạo văn bản, chuyển đổi định dạng, đính kèm, mã định danh, mức khẩn, cấp số tự động, thông báo
    đã nhận, trạng thái xử lý, theo dõi hạn, phân phối, sửa/trả dự thảo, liên thông;
  - quản trị phân quyền, thay đổi quyền, sao lưu/phục hồi, cảnh báo xung đột, đóng băng/thu hồi và
    bảo toàn dữ liệu đặc tả;
  - xuất sổ đăng ký văn bản đến/đi, báo cáo giải quyết, mục lục văn bản/hồ sơ;
  - chuẩn thông tin đầu vào văn bản đi tại Phần II Mục I: mã hồ sơ, thứ tự trong hồ sơ, tên loại,
    số, ký hiệu, ngày, cơ quan ban hành, trích yếu, ngôn ngữ, số trang, ghi chú, chức vụ/họ tên
    người ký, nơi nhận, mức khẩn/mật, số bản phát hành và hạn trả lời. Văn bản đến và hồ sơ có bộ
    trường riêng tại các Mục II-III.
- Các yêu cầu về ký số, chứng thư, định dạng gói tin, kết nối liên thông và bảo vệ bí mật nhà nước
  còn dẫn chiếu pháp luật chuyên ngành/liên quan. Không được kết luận “tuân thủ Phụ lục VI” chỉ từ
  việc app tạo được PDF hoặc có nút Export.

## Ranh giới với báo cáo học thuật và hướng dẫn của đơn vị

- Nghị định 30 là chuẩn văn thư cho đối tượng tại Điều 2. Báo cáo bài tập, luận văn, bài nghiên cứu
  hoặc báo cáo nội bộ không do cơ quan/tổ chức thuộc phạm vi phát hành không tự động chịu toàn bộ
  quy trình văn thư. Trường/viện có thể ban hành hướng dẫn riêng về bìa, mục lục, trích dẫn, font,
  khoảng cách, logo, đánh số chương hoặc mẫu ký xác nhận.
- Khi đơn vị yêu cầu “theo Nghị định 30”, cần ghi rõ mức áp dụng: (a) chỉ áp dụng thể thức và kỹ
  thuật trình bày; (b) áp dụng thêm quy trình duyệt/ký/phát hành; hoặc (c) dùng Hệ thống quản lý tài
  liệu điện tử theo Phụ lục VI. Ba mức này có bằng chứng nghiệm thu khác nhau.
- Hướng dẫn sử dụng app nên gọi sản phẩm chưa ký/phát hành là “bản nháp” hoặc “bản dự thảo”; việc
  app cảnh báo thiếu Quốc hiệu, số, ngày, chữ ký, nơi nhận chỉ là kiểm tra hỗ trợ. Kết luận pháp lý
  cuối cùng thuộc cơ quan/người có thẩm quyền và mẫu được đơn vị phê duyệt.

## Kết quả kiểm tra app của Codex Control

### Các phát hiện cần xử lý trước khi tuyên bố hỗ trợ văn bản hành chính chuẩn

| ID  | Kết quả                                               | Phát hiện và bằng chứng                                                                                                                                                                                                                                                                                                                               |
| --- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| N01 | FAIL                                                  | Mẫu công sở dùng `[[COVER]]`, mục lục và thân báo cáo chung; mẫu biên bản chỉ có ba nhóm nội dung. Không tạo Quốc hiệu/Tiêu ngữ, số-ký hiệu, địa danh-ngày ban hành, tên loại/trích yếu và khối ký/nơi nhận đúng thể thức. Mẫu xuất thực tế xác nhận các thành phần đó vắng mặt.                                                                      |
| N02 | FAIL                                                  | `set_page_numbering()` đặt PAGE trong footer. PDF biên bản hiện 1 và 2 ở chân hai trang, gồm trang đầu; mẫu báo cáo có số La Mã ở mục lục rồi bắt đầu lại 1 ở thân. Quy tắc Phụ lục I, Phần I, Mục I.7 yêu cầu chữ số Ả Rập, cỡ 13-14, giữa lề trên và ẩn số trang đầu.                                                                               |
| N03 | FAIL                                                  | PDF bìa công sở có tiêu đề Calibri 26; heading cấp 1 trong thân và biên bản là Times New Roman 15. `configure_styles()` gán font nhưng giữ tham chiếu theme; style Title sau renderer vẫn chứa `majorHAnsi` và Calibri. Font toàn văn và cỡ/kiểu tên loại, trích yếu, mục của văn bản hành chính chưa được bảo đảm.                                   |
| N04 | FAIL                                                  | GUI metadata công sở chỉ có title, organization, department, author, recipient, period, date. Thiếu trường số-ký hiệu, địa danh, người ký/chức vụ/quyền ký và danh sách nơi nhận; date và recipient không bắt buộc. Mẫu biên bản chỉ bắt buộc title/author, không bắt buộc organization/date. `author` chưa thể đại diện cho người có thẩm quyền ký.  |
| N05 | FAIL                                                  | `project_issues()` chỉ kiểm tra metadata theo config, chương, placeholder và DOCX mẫu. Không kiểm tra tiêu chí pháp lý/font/lề/số trang. Mẫu Arial 10, lề trên/trái 1 cm, giãn dòng 2 được xuất DOCX/PDF `final`, không cảnh báo. Đây là lỗ hổng của việc coi `final` là xác nhận tuân thủ, dù chế độ này vẫn làm đúng kiểm tra nội dung đã khai báo. |
| N06 | FAIL trong phạm vi mẫu hành chính                     | Chưa có mẫu công văn, tờ trình hoặc quyết định để kiểm chứng khác biệt tên loại/trích yếu, ký hiệu, căn cứ và quyền ký. Mẫu báo cáo/biên bản hiện có chưa bám mẫu trình bày Phụ lục III. App không cần hỗ trợ mọi loại văn bản, nhưng cần công bố đúng tập loại thực sự đạt nghiệm thu.                                                               |
| N07 | NOT_EVALUATED                                         | Chưa nghiệm thu nội dung viết hoa, viết tắt, viện dẫn pháp lý và lựa chọn cách đánh số phần/chương/mục theo Phụ lục II-III trên văn bản thật. Không có kết quả tuân thủ các quy tắc này từ bộ test hiện tại.                                                                                                                                          |
| N08 | NOT_EVALUATED; ngoài phạm vi trình soạn thảo hiện tại | Chưa có bằng chứng cho luồng duyệt/ký, chữ ký số của người có thẩm quyền và cơ quan, cấp số/đăng ký, phát hành hoặc lưu trữ theo Hệ thống. Không coi khả năng tạo DOCX/PDF là đáp ứng Phụ lục VI.                                                                                                                                                     |

Căn cứ cho N01-N05: Điều 8-9 và Phụ lục I, Phần I, Mục I.3-I.7, II.1-II.9; N06-N07: Phụ lục II-III;
N08: Điều 5, 10-19 và Phụ lục VI của
[bản Nghị định đã ký](https://datafiles.chinhphu.vn/cpp/files/vbpq/2020/03/30.signed.pdf). Control
đã xem trực tiếp các trang PDF 21-22 và 24-25 của bản gốc để đối chiếu khổ/lề/font, số trang, đầu
văn bản, tên loại và định dạng phần nội dung.

Nguồn mã cho các phát hiện:

- N01/N04/N06: [config công sở](../../templates/bao_cao_cong_so/config.yaml),
  [bìa công sở](../../templates/bao_cao_cong_so/boilerplate/F00_header.md),
  [config biên bản](../../templates/bien_ban/config.yaml),
  [khung biên bản](../../templates/bien_ban/boilerplate/Ch01_Bien_Ban.md);
  [form metadata](../../src/ui/visual_builder/window.py), dòng 372-392.
- N02/N03: [report_fields.py](../../src/core/report_fields.py), `configure_styles` dòng 57-82,
  `set_page_numbering` dòng 85-97, `add_report_cover` dòng 120-143;
  [docx_builder.py](../../src/core/docx_builder.py), xử lý heading dòng 347-375.
- N05: [export.py](../../src/core/export.py), `project_issues` dòng 50-70, kiểm tra final dòng
  217-219/266-267; [config.py](../../src/core/config.py), `settings` là dictionary chung;
  [GUI settings](../../src/ui/visual_builder/window.py), dòng 1654-1722.

### Những phần đạt trên mẫu mặc định

| Hạng mục                   | Kết quả và giới hạn                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Khổ giấy/lề                | PASS trên công sở và biên bản: A4; trên/dưới khoảng 25 mm, trái 30 mm, phải 20 mm. Sai lệch rất nhỏ do đơn vị twip. Chưa có cơ chế chặn người dùng đổi sang giá trị ngoài quy định.                |
| Lời văn                    | PASS trên đoạn mẫu: Times New Roman 13, căn đều hai lề, thụt đầu 1,27 cm, cách đoạn 6 pt; giãn dòng công sở 1,3, biên bản 1,5. Không gộp tiêu đề và chữ ở các thành phần thể thức vào kết quả này. |
| Màu chữ                    | PASS trên cả ba PDF: toàn bộ 1.948 glyph được pdfplumber nhận diện có màu `(0,0,0)`; DOCX ghi màu chữ 000000. Không coi đường kẻ xanh trên bìa là chữ màu xanh.                                    |
| Bảo toàn/kiểm tra nội dung | App có dùng chung export core, kiểm tra chương/metadata khai báo/placeholder, draft/final, field và nội dung PDF. Các chức năng này hữu ích nhưng không thay thế kiểm tra thể thức Nghị định 30.   |
| Hướng dẫn sử dụng          | README đã mô tả các mẫu là khung có thể chỉnh theo đơn vị; chưa có cơ sở coi chúng là mẫu hành chính đạt chuẩn. Việc giữ phạm vi này trong tài liệu hiện tại là phù hợp.                           |

### Thử nghiệm thực tế và khả năng truy vết

Bản sao kiểm tra tại `C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9`. 61 file
source/mẫu liên quan được so hash với workspace, không có khác biệt; danh sách hash ở
[source-provenance.json](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/source-provenance.json).
Mọi dự án và thao tác thử nghiệm nằm trong bản sao này; không dùng báo cáo đang làm của người dùng.

| Ca kiểm tra                 | Kết quả quan sát                                                                                                                             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Công sở                     | 3 trang; chỉ điền title/organization/author, date/recipient trống; thiếu đầu/cuối thể thức hành chính; final thành công, không cảnh báo.     |
| Biên bản                    | 2 trang; chỉ điền title/author; không điền organization/date; không có khối ký/nơi nhận; final thành công, không cảnh báo.                   |
| Biên bản cố ý sai định dạng | Arial 10, lề trên/trái 1 cm, giãn dòng 2; final thành công, không cảnh báo.                                                                  |
| GUI source                  | Mở editor và form thông tin thật bằng Tkinter; đối chiếu đúng 7 trường metadata. Chụp riêng cửa sổ app/form, không chụp màn hình toàn máy.   |
| Kiểm tra phần mềm hiện có   | Bộ pytest trong bản sao: 108 passed, 1 skipped, 1 warning; Ruff src/tests PASS. Các test này không phải bộ nghiệm thu tuân thủ Nghị định 30. |

[Kết quả cấu trúc DOCX, chữ/font/màu/vị trí PDF và SHA-256 từng artifact](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/audit-results.json).
Các bản xuất và ảnh đã xem:

- [Công sở PDF](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/office/build/office.pdf),
  [DOCX](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/office/build/office.docx).
- [Biên bản PDF](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/minutes/build/minutes.pdf),
  [DOCX](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/minutes/build/minutes.docx).
- [Mẫu sai định dạng PDF](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/invalid_format/build/invalid_format.pdf).
- [Form metadata](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/source-metadata.png),
  [editor source](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/source-editor.png),
  [bằng chứng GUI](C:/Users/Home33/AppData/Local/Temp/doc-suite-nd30-audit-g1nx50q9/audit-evidence/source-gui.json).

Giới hạn và sự cố đã xử lý trong phép kiểm tra:

- Lần đầu renderer của mẫu công sở hết thời hạn sẵn sàng; một lần xuất lại thành công sau các mẫu
  biên bản. Không sửa renderer; đây vẫn là sự cố khởi động quan sát được.
- Bản sao test ban đầu thiếu helper `split_chapters.py`; đã bổ sung nguyên trạng các file Python ở
  gốc rồi chạy lại toàn bộ. Kết quả cuối là 108 passed/1 skipped, không dùng kết quả thiếu helper
  làm lỗi của app. Test native conversion bị skip do không khởi tạo được display.
- Script đọc DOCX sau LibreOffice gặp giá trị alignment `start` mà python-docx không ánh xạ; đã đọc
  XML thô. Hai ca biên bản đã xuất thành công từ trước; chỉ đọc lại artifact, không hiểu lỗi của
  script kiểm tra là lỗi xuất của app.
- Không có thư mục dist/EXE được nhắc trong TASK ở worktree này; không tìm hoặc thay thế bản đang
  dùng ở nơi khác. Kiểm tra EXE, input desktop và các đường GUI/CLI/API/batch đóng gói với bộ tiêu
  chí pháp lý: NOT_EVALUATED trong phiên này.
- Chữ ký số, chứng thư, cấp số và quy trình của cơ quan: NOT_EVALUATED. Tài liệu riêng của trường/cơ
  quan không thuộc phạm vi người dùng vừa xác nhận.

### Đề xuất khắc phục để nghiệm thu lần tiếp theo

1. Định nghĩa rõ nhóm văn bản hành chính được hỗ trợ; tạo mẫu báo cáo/biên bản theo Phụ lục III, với
   các thành phần đầu/cuối, metadata và vùng ký phù hợp. Giữ mẫu học thuật ở đúng phạm vi đã công
   bố.
2. Áp dụng styles cho từng thành phần; xử lý font theme/Title; sửa số trang ở lề trên, chữ số Ả Rập,
   ẩn trang đầu và đánh liên tục trong một văn bản hành chính.
3. Bổ sung kiểm tra trước xuất cho nhóm mẫu hành chính: thể thức, giá trị lề/font/đoạn, ngày/địa
   danh/số-ký hiệu, khối ký/nơi nhận. Dự thảo chưa ký vẫn là dự thảo; xác nhận định dạng phải tách
   khỏi trạng thái đã ký/ban hành.
4. Nghiệm thu bằng ca đúng và ca cố ý sai, xem DOCX/PDF thật, chạy các entrypoint chung và EXE đúng
   hash. Chỉ mở rộng sang duyệt/ký số/phát hành/lưu trữ nếu sản phẩm được giao phạm vi đó; khi ấy có
   bộ nghiệm thu riêng theo Phụ lục VI.

Các mục trên là đề xuất sau rà soát, chưa được triển khai trong phiên này. Prettier cho review,
PLAN.md và TASK.md PASS; `git diff --check` PASS. Chỉ ba tài liệu này thay đổi trong workspace.
