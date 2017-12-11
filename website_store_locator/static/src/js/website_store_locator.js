odoo.define('website_store_locator.website_store_locator', function(require) {
    "use strict";
    $(function() {

        var ajax = require('web.ajax');
        var core = require('web.core');
        var _t = core._t;
        var markers = [];
        var infowindows = [];
        var openinfo = null;
        var mapProp;
        var map;
        var vals = {};
        var carrier_value;
        var show_locator;
        var initialize_data;
        var load_count = 0;
        var shop_count = 0;
        var bounds;
        var search_radius = 0;

        show_locator = $('#show-store-locator').data('show-store-locator');
        if (show_locator === 'yes') {
            carrier_value = parseInt($('#carrier-value').data('carrier-value'), 10);
            $('.store_locator_loder').show();
            if (carrier_value) {
                vals = {
                    'carrier_value': carrier_value
                }
            }
            locator_call_json(vals); //fucntion call
            $('.reset-loc').on('click', function() {
                reset_locator_data();
            });

            $('.search-store').on('click', function() {
                search_by_address_init();
            });

            $('#search-input').keypress(function(e) {
                if (e.which == 13) {
                    search_by_address_init();
                }
            });
        }

        function search_by_address_init() {
            var addr_dict = {};
            var search_string = ($('#search-input').val()).toLowerCase();
            $('.store-not-found').hide();
            $('.extra-information').hide();
            hide_info_window();
            search_by_address(search_string);
        }

        function search_by_address(search_string) {
            var main_addr = '';
            var count = 0;
            var not_have_cat = 0;
            bounds = new google.maps.LatLngBounds();
            $.each(initialize_data.map_stores_data, function(key, value) {
                main_addr = get_search_main_address(value);
                if (!main_addr) {
                    main_addr = ''
                }
                var match = main_addr.indexOf(search_string);
                if (match >= 0) {
                    show_marker_and_shop(parseInt(key));
                    count++;
                } else {
                    hide_marker_and_shop(parseInt(key));
                }
            });
            if (count >= 1) {
                map.fitBounds(bounds);
            } else {
                get_shop_nearest_address(search_string);
            }
            $(".store-lable").text("" + count + _t(" Store(s)"));
        }

        function get_shop_nearest_address(search_string) {
            var latitude = 0;
            var longitude = 0;
            var geocoder = new google.maps.Geocoder();
            var count = 0;
            $('.store_locator_loder').show();
            bounds = new google.maps.LatLngBounds();
            geocoder.geocode({
                'address': search_string
            }, function(results, status) {
                $('.store_locator_loder').hide();
                if (status == google.maps.GeocoderStatus.OK) {
                    latitude = results[0].geometry.location.lat();
                    longitude = results[0].geometry.location.lng();
                    $.each(initialize_data.map_stores_data, function(key, value) {
                        var d = distance_between_points(latitude, longitude, value.store_lat, value.store_lng);
                        if (d <= search_radius) {
                            show_marker_and_shop(parseInt(key));
                            count++;
                        } else {
                            hide_marker_and_shop(parseInt(key));
                        }
                    });
                    if (count == 0) {
                        $('.store-not-found').show();
                    } else {
                        map.fitBounds(bounds);
                        $('.extra-information.alert-info').html("Result not found for zip <b><i style='color: #ff0000;'>" + search_string + "</i></b>, showing results for nearest shop form your serach.");
                        $('.extra-information').show();
                    }
                    $(".store-lable").text("" + count + _t(" Store(s)"));
                } else {
                    $('.store-not-found').show();
                }
            });
        }

        function distance_between_points(lat1, lon1, lat2, lon2) {
            var R = 6371; // Radius of the earth in km
            var dLat = deg2rad(lat2 - lat1); // deg2rad below
            var dLon = deg2rad(lon2 - lon1);
            var a =
                Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            var d = R * c * 1000; // Distance in meter
            return d;
        }

        function deg2rad(deg) {
            return deg * (Math.PI / 180)
        }

        function get_search_main_address(store) {
            var main_addr = store.store_name.toLowerCase();
            if (store.store_address[0])
                main_addr += store.store_address[0].toLowerCase() + ' ';
            if (store.store_address[1])
                main_addr += store.store_address[1].toLowerCase() + ' ';
            if (store.store_address[2])
                main_addr += store.store_address[2].toLowerCase() + ' ';
            if (store.store_address[3])
                main_addr += store.store_address[3].toLowerCase() + ' ';
            if (store.store_address[4])
                main_addr += store.store_address[4].toLowerCase() + ' ';
            return main_addr
        }

        function locator_call_json(vals) {
            $('.store_locator_loder').show();
            ajax.jsonRpc('/store/locator/vals', 'call', vals)
                .then(function(data) {
                    if (data) {
                        if (load_count == 0) {
                            initialize_data = data;
                            search_radius = data.map_search_radius;
                        }
                        initialize_store_locator(initialize_data); //fucntion call
                        load_count++;
                    } else {
                        alert(_t("No Store Found."));
                    }
                    $('.store_locator_loder').hide();
                });
        }

        function hide_info_window() {
            if (openinfo != null) {
                infowindows[openinfo].close(map, markers[openinfo]);
                $('#' + (openinfo + 1) + '').find('.store-list').removeClass('selected');
                openinfo = null;
            }
        }

        function initialize_store_locator(initialize_data) {
            var mapProp = {
                center: new google.maps.LatLng(initialize_data.map_init_data.map_center_lat, initialize_data.map_init_data.map_center_lng),
                zoom: initialize_data.map_init_data.map_zoom,
                mapTypeId: initialize_data.map_init_data.map_type
            };
            map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
            draw_marker_and_info_map(map, initialize_data.map_stores_data); //function call
            $('.store-menu ul').append("<li class='store-not-found' style='display:none;'>No Result Found.</li>");
        }

        function draw_marker_and_info_map(map, map_stores_data) {
            $(".store-lable").text("" + Object.keys(initialize_data.map_stores_data).length + _t(" Store(s)"));
            shop_count = ((Object.keys(initialize_data.map_stores_data).length) - 1);
            $.each(map_stores_data, function(key, values) {
                markers.push(new google.maps.Marker({
                    position: new google.maps.LatLng(values.store_lat, values.store_lng),
                    title: values.store_name,
                    map: map,
                    icon: '/website_store_locator/static/src/img/location_marker.png',
                    animation: google.maps.Animation.DROP
                }));
                key = parseInt(key);
                var info = get_store_info_html(values);
                infowindows.push(new google.maps.InfoWindow({
                    content: info
                }));
                load_shop_list(key, values, info);
                markers[key].addListener('click', function() {
                    if (openinfo != null) {
                        infowindows[openinfo].close(map, markers[openinfo]);
                        $('#' + (openinfo + 1) + '').find('.store-list').removeClass('selected');
                        openinfo = null;
                    }
                    infowindows[key].open(map, markers[key]);
                    if (!markers[key].getVisible()) {
                        markers[key].setVisible(true);
                    }
                    $('#' + (key + 1) + '').find('.store-list').addClass('selected');
                    openinfo = key;
                    var temp = $(".store-menu").offset().top;
                    $(".store-menu").animate({
                        scrollTop: 0
                    }, 1, function() {
                        $(".store-menu").animate({
                            scrollTop: $('#' + (key + 1) + '').offset().top - temp
                        }, 1);
                    });
                });
            });
        }

        function get_store_info_html(store) {
            var addr = '';
            if (store.store_image) {
                addr += '<div class="store-image"><img style="max-height:70px;" src="' + store.store_image + '"/></div>';
            }
            if (store.store_name) {
                addr += '<div style="font-weight:900; font-size:16px;">' + store.store_name + '</div> <div style="font-weight:400;">';
            }
            if (store.store_address[0]) {
                addr += store.store_address[0] + '<br/>';
            }
            if (store.store_address[1]) {
                addr += store.store_address[1] + ', ';
            }
            if (store.store_address[2]) {
                addr += store.store_address[2] + ', ';
            }
            if (store.store_address[3]) {
                addr += store.store_address[3] + '<br/>';
            }
            if (store.store_address[4]) {
                addr += store.store_address[4] + '<br/>';
            }
            if (store.store_address[6] || store.store_address[7]) {
                addr += '<div class="store-contact"> <b>Tel: </b>'
                if (store.store_address[6]) {
                    addr += store.store_address[6];
                }
                if (store.store_address[6] && store.store_address[7]) {
                    addr += ', ';
                }
                if (store.store_address[7]) {
                    addr += store.store_address[7]
                }
                addr += '</div>';
            }
            if (store.store_address[8]) {
                addr += '<div class="store-contact"><b>Fax: </b>' + store.store_address[8] + '</div>';
            }
            if (store.store_address[9]) {
                addr += '<div class="store-contact"><b>Email: </b><a href="mailto:' + store.store_address[9] + '">' + store.store_address[9] + '</a></div>';
            }
            if (store.store_address[5]) {
                addr += '<div class="web-addr"><b>www:</b> <a target="_blank" href="' + store.store_address[5] + '">' + store.store_address[5] + '</a></div>';
            }
            addr += '</div>'
            return addr;
        }

        function load_shop_list(key, store, info) {
            $('.store-menu ul').append("<li id=" + (key + 1) + " class=''>\
            <div class='store-list'>\
              <span id='map-lat' data-map-lat=" + store.store_lat + "/>\
              <span id='map-lng' data-map-lng=" + store.store_lng + "/>\
              <input type='hidden' name='store-id' value=" + store.store_id + "></input>\
              <div class='list-image col-md-2 col-sm-4 col-xs-4'>\
                <img style='height: 38px' src='/website_store_locator/static/src/img/location.png'/>\
              </div>\
              <div class='store-info col-md-10'>" + info + "</div>\
            </div></li>");
            $('li#' + key + '').find('.store-info img').remove();

            $('#' + (key + 1) + '').on('click', function() {
                if (openinfo != null) {
                    infowindows[openinfo].close(map, markers[openinfo]);
                    $('#' + (openinfo + 1) + '').find('.store-list').removeClass('selected');
                    openinfo = null;
                }
                $('#' + (key + 1) + '').find('.store-list').addClass('selected');
                map.setZoom(11);
                markers[key].setVisible(true);
                map.setCenter(markers[key].getPosition());
                infowindows[key].open(map, markers[key]);
                openinfo = key;
            });
        }

        function reset_locator_data() {
            $('.store-not-found').hide();
            $('#search-input').val('');
            $('.extra-information').hide();
            map.setZoom(initialize_data.map_init_data.map_zoom);
            map.setCenter(new google.maps.LatLng(initialize_data.map_init_data.map_center_lat, initialize_data.map_init_data.map_center_lng));
            if (openinfo != null) {
                infowindows[openinfo].close(map, markers[openinfo]);
                $('#' + (openinfo + 1) + '').find('.store-list').removeClass('selected');
                openinfo = null;
            }
            show_all_initial_marker(); //function call
            show_all_shop_list(); //function call
        }

        function show_all_initial_marker() {
            $.each(markers, function(index, value) {
                if (!value.getVisible()) {
                    value.setVisible(true);
                }
            });
        }

        function show_all_shop_list() {
            $('.store-menu ul li').removeClass('shop-hidden');
            $(".store-lable").text("" + Object.keys(initialize_data.map_stores_data).length + _t(" Store(s)"));
            shop_count = ((Object.keys(initialize_data.map_stores_data).length) - 1);
        }

        function show_marker_and_shop(key) {
            if (!markers[key].getVisible()) {
                markers[key].setVisible(true);
            }
            bounds.extend(markers[key].getPosition());
            $('#' + (key + 1) + '').removeClass('shop-hidden');
        }

        function hide_marker_and_shop(key) {
            if (markers[key].getVisible()) {
                markers[key].setVisible(false);
            }
            $('#' + (key + 1) + '').addClass('shop-hidden');
        }

    });
});