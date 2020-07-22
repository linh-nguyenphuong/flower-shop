class EmailTemplate:
    class EmailConfirmation:
        SUBJECT = '[Flowershop] Kích hoạt tài khoản Flowershop'
        BODY = '''
            <p>Xin chào {0},</p>

            <p>Địa chỉ email này đã được sử dụng để đăng ký tài khoản tại Flowershop!<p>

            <p>
                Xin vui lòng kích hoạt tài khoản bằng cách click vào nút bên dưới:
                <br>
                <a href="{1}" style="background-color:#4BB543;border:1px solid #45a83e;border-radius:3px;color:#ffffff;display:inline-block;font-family:sans-serif;font-size:16px;line-height:44px;text-align:center;text-decoration:none;width:250px;-webkit-text-size-adjust:none;mso-hide:all;">Kích hoạt tài khoản &rarr;</a>
                <br>
                Sau khi kích hoạt thành công, hãy cập nhật thông tin cá nhân chính xác để được bảo vệ các quyền lợi và được hỗ trợ tốt nhất khi sử dụng các dịch vụ và tiện ích của Flowershop.
                <br>
                Lưu ý:
                <br>
                - Nếu trong 7 ngày bạn không kích hoạt tài khoản, hệ thống sẽ tự động hủy tài khoản của bạn.
                <br>
                - Nếu click vào nút trên không thành công, bạn vui lòng copy và paste đường dẫn bên dưới vào cửa sổ trình duyệt bạn đang sử dụng:
                <br>
                <a href="{1}">{1}</a>
                <br>
                - Đây là email được gửi tự động từ hệ thống Flowershop. Bạn không trả lời thư này. Nếu bạn gặp vấn đề trong khi kích hoạt tài khoản, vui lòng liên hệ hỗ trợ theo địa chỉ bên dưới.
                <br>
            </p>
            
            <p>Cảm ơn bạn đã lựa chọn sử dụng dịch vụ của Flowershop.</p>
            <br>
            -----------------------------------------------------
            <br>
            Địa chỉ: Khoa Công nghệ thông tin và Truyền thông, Trường Đại học Cần Thơ - Khu II, Đường 3-2, Xuân Khánh, Ninh Kiều, Cần Thơ.
        '''

    class ForgotPasswordConfirmation:
        SUBJECT = '[Flowershop] Lấy lại mật khẩu qua email'
        BODY = '''
            <p>Xin chào {0},</p>

            <p>
                Vui lòng truy cập {1} để cập nhật lại mật khẩu của bạn.
                <br>
                Lưu ý:
                <br> 
                - Đường link chỉ được sử dụng 01 lần
                <br>
                - Nếu bạn không sử dụng đường link này trong vòng 3 giờ, nó sẽ hết hạn.
                <br>
            </p>
            
            <p>Cảm ơn bạn đã lựa chọn sử dụng dịch vụ của Flowershop.</p>
            <br>
            -----------------------------------------------------
            <br>
            Địa chỉ: Khoa Công nghệ thông tin và Truyền thông, Trường Đại học Cần Thơ - Khu II, Đường 3-2, Xuân Khánh, Ninh Kiều, Cần Thơ.
        '''