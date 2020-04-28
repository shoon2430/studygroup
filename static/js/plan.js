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

const confirm_complete = () => {
    const massge = "결과보고를 제출 하시겠습니까? \n제출 후 수정은 불가능 합니다.";

    const custom_form = document.querySelector('form');
    const next_status_input = document.createElement("input");

    next_status_input.setAttribute("type", "hidden");
    next_status_input.setAttribute("name", "next_status");
    next_status_input.setAttribute("id", "next_status");
    next_status_input.setAttribute("value", "COMPLETE");

    custom_form.append(next_status_input);

    if (confirm(massge)) {
        custom_form.submit();
    }
}

const confirm_success = (func, url) => {
    const massge = "결과를 최종 승인하시겠습니까?";
    func(url, massge);
}

const plan_file_download = (func, url) => {
    func(url);
}

const plan_file_delete = (func, url) => {
    massage = "첨부파일을 삭제 하시겠습니까?";
    func(url, massage);
}
