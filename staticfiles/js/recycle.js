$(document).ready(function () {
    // Initialize Owl Carousel
    $(".owl-carousel").owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        items: 1,
        autoplay: true,
        autoplayTimeout: 5000,
        dots: true
    });

    // Handle slider image clicks
    $(".slider-img").click(function () {
        $(".slider-img").removeClass("active");
        $(this).addClass("active");
    });

    // Toggle between Seller and Buyer Sections
    $("#sellerBtn").click(function () {
        $(this).addClass("active");
        $("#buyerBtn").removeClass("active");
        $("#sellerSection").removeClass("hidden");
        $("#buyerSection").addClass("hidden");
    });

    $("#buyerBtn").click(function () {
        $(this).addClass("active");
        $("#sellerBtn").removeClass("active");
        $("#buyerSection").removeClass("hidden");
        $("#sellerSection").addClass("hidden");
    });

    // Scroll to Top Button
    const $up = $("#up");

    $(window).scroll(function () {
        if ($(this).scrollTop() > 950) {
            $up.addClass("active");
        } else {
            $up.removeClass("active");
        }
    });

    $up.click(function () {
        $("html, body").animate({ scrollTop: 0 }, "smooth");
    });
});
