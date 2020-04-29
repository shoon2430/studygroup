const GROUPS = $("#group_list");
const PAGES = $("#group_page");
const FILTER = $("#filter_btn");


// const group_filtering = (url) => {

//     const search_text = $("#group_search").val();
//     const selected_category = $("#group_category").val();

//     $.ajax({
//         url: url,
//         type: "GET",
//         cache: false,
//         dataType: "json",
//         data: {
//             "search_text": search_text,
//             "selected_category": selected_category
//         },
//         success: function (response) {
//             GROUPS.empty();
//             PAGES.empty();
//             GROUPS.html(response['group_box_html']);
//             PAGES.html(response['group_page_html']);
//         },

//         error: function (request, status, error) {
//             alert(error);
//         }
//     });
// }
