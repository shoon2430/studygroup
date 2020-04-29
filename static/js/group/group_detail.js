const GROUP_USERS = $("#group_users");


const delete_group = (func, url) => {
    const massge = "그룹을 삭제하시겠습니까?";
    func(url, massge);
}

const join_or_exit_group = (func, url, status) => {
    let massage = status == "JOIN" ? "그룹에 참여하시겠습니까?" : "그룹을 나가겠습니까?";

    if (status == "EXIT") {
        user_cnt = GROUP_USERS.find(".user").length
        if (user_cnt == 1) {
            massage = "현재 그룹에 다른 인원이 없으므로\n그룹을 나갈시 그룹이 삭제됩니다.";
        }
    }
    func(url, massage);
}