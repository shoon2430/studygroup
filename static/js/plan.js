const plan_delete = (func) => {
    url = "{%url 'groups:plan-delete' plan.group.pk plan.pk %}";
    massage = "계획을 삭제하시겠습니까?";
    func(url, massage);
}

const plan_confirm = (func) => {
    url = "{%url 'groups:plan-change-status' plan.group.pk plan.pk %}";
    massage = "계획을 승인하시겠습니까?";
    data = {
        "next_status": "CONFIRM"
    };
    func(url, massage, data);
}

const confirm_success = (func) => {
    const massge = "결과를 최종 승인하시겠습니까?";
    const url = "{%url 'groups:plan-feedback' plan.group.pk plan.pk%}";
    func(url, massge);
}
