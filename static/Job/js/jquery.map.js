function initMap() {
  // Define an array to hold your dynamic location data (e.g., from JSON)
  var locations = [
    {
      lat: 37.7749,
      lng: -122.4194,
      imageSrc: 'images/img_90.jpg',
      // name: "San Francisco, CA",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 34.0522,
      lng: -118.2437,
      imageSrc: 'images/img_89.jpg',
      // name: "Los Angeles, CA",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 40.7128,
      lng: -74.0060,
      imageSrc: 'images/img_88.jpg',
      // name: "New York, NY",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 39.0997,
      lng: -94.5786,
      imageSrc: 'images/img_90.jpg',
      // name: "Kansas City",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 36.1716,
      lng: -115.1391,
      imageSrc: 'images/img_89.jpg',
      // name: "Las Vegas",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 41.8781,
      lng: -87.6298,
      imageSrc: 'images/img_88.jpg',
      // name: "Chicago",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
    {
      lat: 32.7767,
      lng: -96.7970,
      imageSrc: 'images/img_90.jpg',
      // name: "Dallas",
      // description: "This is a description text.",
      // phone: "+1 212 456 7890",
      // siteLink: "<a href='https://www.google.com/' target='_blank'>Site Link</a>",
    },
  ];

  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 5,
    center: { lat: 37.0902, lng: -95.7129 }, // United States coordinates
  });

  var infowindow = new google.maps.InfoWindow();

  // Create custom markers and info windows for your dynamic location data
  for (var i = 0; i < locations.length; i++) {
  (function (i) {
    var marker = new google.maps.Marker({
      position: { lat: locations[i].lat, lng: locations[i].lng },
      map: map,
      title: locations[i].name,
      icon: {
        url: "images/map-ping.png", // Custom pin image URL
        scaledSize: new google.maps.Size(30, 42), // Set the width and height
      },
    });

    // Create a content string for the info window
    var contentString =
      "<div class='map-tooltip'>" +
      "</div>";

      google.maps.event.addListener(marker, "click", function () {
        var geocoder = new google.maps.Geocoder();
        var latlng = { lat: locations[i].lat, lng: locations[i].lng };
      
        geocoder.geocode({ location: latlng }, function (results, status) {
          if (status === "OK") {
            if (results[0]) {
              // Find the city name in address components
              var cityName = "";
              for (var j = 0; j < results[0].address_components.length; j++) {
                for (var k = 0; k < results[0].address_components[j].types.length; k++) {
                  if (results[0].address_components[j].types[k] === "locality") {
                    cityName = results[0].address_components[j].long_name;
                    break;
                  }
                }
              }
      
              // Concatenate location name, image, and address from geocoding results
              var locationInfo =
                "<div class='map-tooltip'>" +
                "<div class='tooltip-image'>" +
                "<img src='" + locations[i].imageSrc + "' alt='Image Description'>" +
                "</div>" +
                "<strong class='tooltip-title'>" + cityName + "</strong>" +
                "<p class='location-address'><span class='fa-solid fa-location-dot address-pin'></span> " + "<span class='address-text'>" + results[0].formatted_address + "</span></p>"
                "</div>";
      
              // Create a new contentString for each click
              var newContentString = contentString + locationInfo;
              infowindow.setContent(newContentString);
              infowindow.open(map, marker);
            } else {
              console.error("No results found");
            }
          } else {
            console.error("Geocoder failed due to: " + status);
          }
        });
      });      
    })(i);
  }
}