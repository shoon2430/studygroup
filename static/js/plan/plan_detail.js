const plan_delete = (func, url) => {
    massage = "계획을 삭제하시겠습니까?";
    func(url, massage);
}

const plan_confirm = (func, url) => {
    massage = "계획을 승인하시겠습니까?";
    data = {
        "next_status": "CONFIRM"
    };
    func(url, massage, data);
}


const plan_file_delete = (func, url) => {
    massage = "첨부파일을 삭제 하시겠습니까?";
    func(url, massage);
}

