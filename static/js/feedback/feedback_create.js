const RATING = document.getElementById("id_rating");

$('.starRev span').click(function () {
    $(this).parent().children('span').removeClass('on');
    $(this).addClass('on').prevAll('span').addClass('on');

    RATING.value = $('.on').length;
    return false;
});


const plan_success = (func) => {
    url = "{%url 'groups:plan-change-status' plan.group.pk plan.pk %}";
    massage = "승인하시겠습니까?";
    data = {
        "next_status": "SUCCESS"
    };
    func(url, massage, data);
}
