$(document).ready(function(){
    var toast = $("#result_toast")[0].MaterialSnackbar
    var ban = $("#ban")
    var unban = $("#unban")
    $("#ban_link").css("overflow", "hidden").autogrow({horizontal: false})

    ban.submit(function(){
        $.post(
            ban.attr("action"),
            ban.serialize(),
            function(data, status, xhr){
                toast.showSnackbar({message: data})
            }
        )
        return false
    })

    unban.submit(function(){
        $.post(
            unban.attr("action"),
            unban.serialize(),
            function(data, status, xhr){
                toast.showSnackbar({message: data})
            }
        )
        return false
    })
})