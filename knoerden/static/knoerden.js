
$.when($.ready).done(init);

function init() {
    console.log("in init");
    var login_modal = $("#login");
    var login_button = $("#login_btn");
    var login_close = $("#login, #login .close");
    login_button.on("click", (e) => {
        login_modal.show();
        e.preventDefault();
        return false;
    });
    login_close.on("click", (event) => {
        if ($(event.target).is(login_close)) {
            login_modal.hide();
        }
    });
};
