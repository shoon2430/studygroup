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

const confirm_complete = (func, url) => {
    const massge = "결과보고를 제출 하시겠습니까? \n제출 후 수정은 불가능 합니다.";
    const data = {
        "next_status": "COMPLETE"
    };
    func(url, massge, data);
}


const confirm_success = (func, url) => {
    const massge = "결과를 최종 승인하시겠습니까?";
    func(url, massge);
}
