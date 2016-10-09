$(document).ready(function(){
    var dialog = $("#view")[0],
        result_image = $("#result_image"),
        go = $("#go"),
        font_slider = $("#font_slider"),
        size = $("#size")

    new Clipboard("#copy_link")

    font_slider.on("input", function() {
        size.prop("value", font_slider.val())
    })

    size.on("input", function(){
        var value = size.val()
        if (!value) {
            value = 0
        }
        font_slider.MaterialSlider.change(value)
    })

    $("#close_dialog").click(function(){
        $("#loading").addClass("is-active")
        result_image.attr("src", "")
        result_image.css("visibility", "hidden")
        dialog.close()
    })

    go.submit(function(){
        var error = true
        dialogPolyfill.registerDialog(dialog)
        dialog.showModal()
        $.post(
            go.attr("action"),
            go.serialize(),
            function(data){
                $("#loading").removeClass("is-active")
                result_image.attr("src", data)
                result_image.css("visibility", "visible")
                $("#copy_link").attr("data-clipboard-text", data)
                error = false
            }
        )
        return !error
    })
})
