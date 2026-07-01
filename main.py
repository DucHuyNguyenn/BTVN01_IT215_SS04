from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Dữ liệu giả lập
students = [
    {
        "full_name": "Nguyen Van A",
        "email": "vana@gmail.com",
        "age": 20,
        "course": "Python",
        "phone": "0987654321"
    },
    {
        "full_name": "Tran Thi B",
        "email": "tranb@gmail.com",
        "age": 21,
        "course": "Java",
        "phone": "0912345678"
    }
]


class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., gt=0)
    course: str = Field(..., min_length=3)
    phone: str = Field(..., pattern=r"^\d{10}$")


@app.get("/")
def home():
    return {
        "message": "Student API"
    }


@app.get("/students", status_code=status.HTTP_200_OK)
def get_students():
    return {
        "status": "Success",
        "message": "Lấy danh sách thành công",
        "students": students
    }


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):

    # Kiểm tra email đã tồn tại
    for stu in students:
        if stu["email"] == student.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email đã tồn tại trong hệ thống"
            )

    new_student = student.model_dump()

    students.append(new_student)

    return {
        "status": "Success",
        "message": "Tạo học viên thành công",
        "student": new_student
    }

# Giải pháp 1: Validate thủ công
# Nhận dữ liệu dạng dict.
# Tự kiểm tra từng trường bằng if.
# Tự kiểm tra email bằng regex.
# Tự kiểm tra dữ liệu thiếu.

# Ưu điểm

# Linh hoạt.
# Hiểu rõ quá trình validate.

# Nhược điểm

# Code dài.
# Dễ sai.
# Khó bảo trì.

# Giải pháp 2: Sử dụng Pydantic (đề xuất)
# Khai báo BaseModel.
# Dùng Field() để validate.
# Dùng EmailStr để kiểm tra email.
# Chỉ tự kiểm tra email trùng trong danh sách.

# Ưu điểm

# Code ngắn.
# Dễ đọc.
# FastAPI tự trả lỗi 422.
# Đúng chuẩn FastAPI.

# Nhược điểm

# Cần biết cách khai báo BaseModel.
# Bảng so sánh
# Tiêu chí	Giải pháp 1 (Validate thủ công)	Giải pháp 2 (Pydantic)
# Độ dễ hiểu	Trung bình	Cao
# Số lượng code	Nhiều	Ít
# Khả năng kiểm soát lỗi	Phải tự xử lý	FastAPI hỗ trợ
# Cấu trúc dữ liệu	Không rõ ràng	Rõ ràng với BaseModel

# Kết luận: Chọn Giải pháp 2 vì tận dụng được khả năng validate tự động của Pydantic, giúp mã nguồn ngắn gọn, dễ bảo trì và đúng với cách phát triển API bằng FastAPI. 
# Chỉ cần bổ sung kiểm tra email trùng là đáp ứng đầy đủ yêu cầu của bài toán.