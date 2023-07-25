$(document).click(function () {
    let filled = "fas"
    let empty = "far"
    $(".remFav").click(function () {
        $.ajax({
            url: '/add_to_bookmarked',
            type: 'GET',
            async: false,
            data: {
                text: "Remove From Favorites",
                id: $("#id").text()
            },
            success: function (response) {
                $("#link"+$("#id").text()).removeClass("remFav").removeClass("fas").addClass("addFav "+empty)
            }
        });
    });
    $(".addFav").click(function () {
        $.ajax({
            url: '/add_to_bookmarked',
            type: 'GET',
            async: false,
            data: {
                text: "Add to Favorites",
                id: $("#id").text()
            },
            success: function (response) {
                $("#link"+$("#id").text()).removeClass("addFav").removeClass("far").addClass("remFav "+filled)
            }
        });
    });
});


$(document).ready(function () {
    $("#sort").on("change", function () {
        $.ajax({
            url: "sort_cars",
            type: "GET",
            data: {
                sort_id: $('#sort').val()
            },
            dataType: "json",
            success: function (data) { // On success, display the sorted properties
                displaySortedProperties(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error:", errorThrown);
            }
        });
    });

    function displaySortedProperties(data) {
        var carsContainer = $("#cars");
        carsContainer.empty();
    
        // Loop through the sorted cars and update the HTML
        console.log(data.page)
        data.forEach(function (car) {
            var carDiv = $("<div>").addClass("grid-item");
            var grid = $("<div>").addClass("grid");
    
            // Image
            var imgSrc = "../static/img/Logo1.png"; // You should replace this with the appropriate image URL for each car
            var carImage = $("<img>").addClass("card-img-top").attr("src", imgSrc);
    
            // Card Body
            var cardBody = $("<div>").addClass("card-body");
            var carName = $("<h5>").text(car.name);
            var carModel = $("<span>").text(car.model);
            var carColor = $("<span>").text(car.color);
            var carFuelType = $("<span>").text(car.fuelType);
            var carPrice = $("<span>").text(car.price + "/day");
            var addToCartLink = $("<a>").attr("href", "/book").addClass("btn btn-outline-dark").css("color", "black").text("Add to Cart");
            var bookmarkLink = $("<a>").attr("href", "add_bookmark/" + car.id).html('<i class="fas fa-bookmark"></i>');
    
            cardBody.append(carName, carModel, carColor, $("<br>"), carFuelType, carPrice, $("<br>"), $("<br>"), addToCartLink, bookmarkLink);
    
            // Append elements to the container
            grid.append(carImage, cardBody);
            carDiv.append(grid);
            carsContainer.append(carDiv);
        });
    }
});