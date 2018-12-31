$(document).ready(function() {
    html2canvas($('#content'), {
        onrendered: function (canvas) {
            var base64image = canvas.toDataURL("image/png");
            $('meta[property="og:image"]').attr("content", base64image);
            $('meta[name="twitter:image"]').attr("content", base64image);
        }
    });
});