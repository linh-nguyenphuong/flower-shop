class ErrorTemplate:
    class AuthorizedError:
        ADMIN_REQUIRED = dict(
            success=False,
            message='Yêu cầu đăng nhập bằng tài khoản quản trị.'
        )

        USER_REQUIRED = dict(
            success=False,
            message='Yêu cầu đăng nhập.'
        )

        EMAIL_ALREADY_EXISTED = dict(
            success=False,
            message='Địa chỉ email này đã được sử dụng.'
        )

        INCORRECT_EMAIL = dict(
            success=False,
            message='Không tìm thấy tài khoản sử dụng email này.'
        )

        INCORRECT_PASSWORD = dict(
            success=False,
            message='Mật khẩu không chính xác.'
        )

        USER_NOT_EXIST = dict(
            success=False,
            message='Mã người dùng không tồn tại.'
        )

        PASSWORDS_NOT_MATCH = dict(
            success=False,
            message='Mật khẩu không trùng khớp.'
        )

        EXPIRED_LINK = dict(
            success=False,
            message='Đường dẫn dùng để xác thực này đã hết hạn.'
        )

        VERIFIED_EMAIL_REQUIRED = dict(
            success=False,
            message='Vui lòng xác thực địa chỉ email này để thực hiện đăng nhập.'
        )

        VERIFIED_EMAIL = dict(
            success=False,
            message='Địa chỉ email này đã được xác minh.'
        )

        EMAIL_NOT_EXIST = dict(
            success=False,
            message='Địa chỉ email này chưa tồn tại.'
        )

        INVALID_RESET_PASSWORD_LINK = dict(
            success=False,
            message='Đường dẫn không hợp lệ.'
        )

        FIELDS_REQUIRED = dict(
            success=False,
            message='Vui lòng truyền đầy đủ các trường.'
        )
        
    class AdminError:

        NOT_BLOCK_OLDER_ADMIN = dict(
            success=False,
            message='Không thể khóa tài khoản admin được tạo ra trước tài khoản hiện tại.'
        )

        FLOWER_CATEGORY_ALREADY_EXISTED = dict(
            success=False,
            message='Tên loại hoa đã tồn tại.'
        )

        FLOWER_CATEGORY_NOT_EXIST = dict(
            success=False,
            message='Loại hoa không tồn tại.'
        )

        FLOWER_ALREADY_EXISTED = dict(
            success=False,
            message='Tên hoa đã tồn tại.'
        )

        FLOWER_NOT_EXIST = dict(
            success=False,
            message='Tên hoa không tồn tại.'
        )

        SUPPLIER_ALREADY_EXISTED = dict(
            success=False,
            message='Tên nhà cung cấp đã tồn tại.'
        )

        SUPPLIER_NOT_EXIST = dict(
            success=False,
            message='Nhà cung cấp không tồn tại.'
        )

        GOODS_RECEIPT_NOT_EXIST = dict(
            success=False,
            message='Mã thông tin nhập kho không tồn tại.'
        )

        ORDER_DETAIL_NOT_EXIST = dict(
            success=False,
            message='Mã chi tiết hóa đơn không tồn tại.'
        )

        SHIPPING_NOT_EXIST = dict(
            success=False,
            message='Mã vận chuyển không tồn tại.'
        )

    class UserError:
        CANNOT_UPLOAD_IMAGE = dict(
            success=False,
            message='Không thể tải ảnh lên, xin vui lòng kiểm tra lại.'
        )

        IMAGE_REQUIRED = dict(
            success=False,
            message='Vui lòng tải lên ít nhất 1 ảnh.'
        )

        IMAGE_NOT_EXIST = dict(
            success=False,
            message='Mã hình ảnh không tồn tại.'
        )

        PROFILE_NOT_FOUND = dict(
            success=False,
            message='Không tìm thấy trang thông tin cá nhân.'
        )

        INVALID_IMAGE = dict(
            success=False,
            message='Định dạng hình ảnh không được cho phép.'
        )

        FLOWER_OUT_OF_STOCK = dict(
            success=False,
            message='Loại hoa này đã hết hàng.'
        )

        STOCK_QUANTITY_NOT_ENOUGH = dict(
            success=False,
            message='Số lượng mua vượt quá số lượng còn lại.'
        )

        CANNOT_UPDATE_ORDER_ALREADY_CHECK_OUT = dict(
            success=False,
            message='Không thể cập nhật chi tiết hóa đơn của hóa đơn đã được thanh toán.'
        )

        CANNOT_DELETE_ORDER_ALREADY_CHECK_OUT = dict(
            success=False,
            message='Không thể xóa chi tiết hóa đơn của hóa đơn đã được thanh toán.'
        )

        ORDER_NOT_EXIST = dict(
            success=False,
            message='Mã hóa đơn không tồn tại.'
        )

        CANNOT_SHOW_ORDER_BELONG_OTHER_PERSON = dict(
            success=False,
            message='Không thể xem hóa đơn của người khác.'
        )

        SHIP_DATE_REQUIRED = dict(
            success=False,
            message='Vui lòng nhập ngày giao.'
        )

        ADDRESS_REQUIRED = dict(
            success=False,
            message='Vui lòng nhập địa chỉ giao.'
        )

        EMPTY_ORDER = dict(
            success=False,
            message='Hóa đơn hiện tại chưa có sản phẩm.'
        )
    