$(document).ready(function() {
    html2canvas($('#content'), {
        onrendered: function (canvas) {
            var base64image = canvas.toDataURL("image/png");
            $('meta[property="og:image"]').attr("content", base64image);
            $('meta[property="twitter:card"]').attr("content", base64image);
        }
    });
});