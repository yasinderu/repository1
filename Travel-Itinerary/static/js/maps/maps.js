function initialize() {
        window.map = [];

        function renderDirections(day, result, color) {
          var polylineOptions = {
            strokeColor: color,
            strokeWeight: 5,
            // strokeHeight: 10,
            strokeOpacity: 1.0
          };

          var dr = new google.maps.DirectionsRenderer({
            polylineOptions: polylineOptions,
            map: window.map[day],
            preserveViewport: true
          });

          dr.setDirections(result);
        }

        function requestDirections(day, locations, color, lat, lng, place_id) {
          var elId = 'map_canvas' + day;

          setTimeout(function () {
            window.map[day] = new google.maps.Map(document.getElementById(elId), {
              zoom: 13,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
              center: new google.maps.LatLng(-7.797068, 110.370529)
            });

            var request = {
              travelMode: google.maps.DirectionsTravelMode.DRIVING,
              optimizeWaypoints: true
            };

            if (locations.length > 1) {
              request.waypoints = [];
            };

            var requestDetail = {
              fields: ['name']
            };

            // var service = new google.maps..places.PlacesService(window.map[day]);

            var marker = [];
            for (var i = 0; i < locations.length; i++) {

              if (i == 0 || i == locations.length){
                var content = '<div class="map-marker">' +
                '<div class="loc-detil" style="background-color:' + color + '"></div>' + 
                '<div class="loc-name">' + 'Lokasi Anda' + '<br>';
              }else{
                var content = '<div class="map-marker">' +
                '<div class="loc-detil" style="background-color:' + color + '"></div>' + 
                '<div class="loc-name">' + locations[i] + '<br>';
              }

              if (i == 0 || i == locations.length) {
                content += ' <span>Lokasi Awal & Akhir</span></div>';
              } else {
                content += ' <span>Destinasi ke-' + i + '</span></div>';
              }

              content += '</div>';

              // marker[i] = new RichMarker({
              //   position: new google.maps.LatLng(lat, lng),
              //   map: window.map[day],
              //   content: content,
              //   shadow: 0
              // });

              marker[i] = new RichMarker({
                position: new google.maps.LatLng(lat[i], lng[i]),
                map: window.map[day],
                content: content,
                shadow: 0
              });

              if (i === 0) {
                request.origin = marker[i].getPosition();
              } else if (i === locations.length - 1) {
                request.destination = marker[i].getPosition();
                requestDetail.placeId = place_id[i];
              } else {
                request.waypoints.push({
                  location: marker[i].getPosition(),
                  stopover: true
                });
              }

              // marker[i].info = new google.maps.InfoWindow();
              // var service = new google.maps.PlacesService(window.map[day]);
              // requestDetail.placeId = place_id[i]

              // service.getDetails(requestDetail, function(place, status) {
              //     if (status === google.maps.places.PlacesServiceStatus.OK) {
              //       google.maps.event.addListener(marker[i], 'click', function () {
              //         this.info.setContent('<div><strong>' + place.name + '</strong><br>');
              //         this.info.open(window.map[day], this);
              //       });
              //     }

              //   });
            }

            var ds = new google.maps.DirectionsService();

            ds.route(request, function (response, status) {
              if (status === 'OK') {
                renderDirections(day, response, color);

                // var lastLoc = locations[locations.length - 1];
                request.origin = request.destination;
                request.waypoints = undefined;
                request.destination = locations[locations.length - 1];

                ds.route(request, function (response, status) {
                  if (status === 'OK') {
                    renderDirections(day, response, '#' + color.substr(1).split('').reverse().join(''));
                  } else {
                    console.log('Could not display directions due to: ' + status);
                  }
                });
              } else {
                console.log('Could not display directions due to: ' + status);
              }
            });
          }, 2500);
        }

        var Data = '{{result_json}}';
        var itineraryData = JSON.parse(Data.replace(/&quot;/g, '"'));

        function getRandomColor() {
          var letters = '0123456789ABCDEF';
          var color = '#';
          for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
          }
        return color;
      }

        $('.select-day').click(function() {
          var self = $(this);
          var buttons = $('.select-day');
          var color = getRandomColor();

          buttons.each(function () {
            $(this).removeClass('selected');
          });

          self.addClass('selected');

          var day = $(this).attr('day');

          var boxes = $('.map-box');

          boxes.each(function () {
            $(this).hide();
          });

          $('.map-box-' + day).fadeIn(500);

          var data = itineraryData[day];

          requestDirections(day, data.routes, color, data.lat, data.lng, data.place_id);
        });

        $('.select-day')[0].click();
      }

      google.maps.event.addDomListener(window, 'load', initialize);