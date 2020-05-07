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


const result_file_delete = (url) => {
    massage = "결과의 첨부파일을 삭제 하시겠습니까?";

    if (confirm(massage)) {
        opts = set_POST();

        fetch(url, opts)
            .then(function (response) {
                alert("삭제되었습니다");
                window.location.reload(true);
            });
    }
}

