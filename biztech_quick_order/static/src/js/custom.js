odoo.define('biztech_quick_order.custom_js', function(require) {
    'use strict';
    var ajax = require('web.ajax');

    $(document).ready(function() {
        'use strict';

        $('[data-toggle="tooltip"]').tooltip({
            placement: 'top'
        });

        var url_to_del_localstorage = window.location.href.indexOf('quickorder')
        if (url_to_del_localstorage < 0) {
            localStorage.removeItem('product_list')
            localStorage.removeItem('product_price')
        }
        if (!localStorage['product_list']) {
            var add_list = {}
            localStorage.setItem('product_list', JSON.stringify(add_list));
        }
        if (localStorage['product_list']) {
            var prop
            var storage = JSON.parse(localStorage['product_list'])
            for (prop in storage) {
                var $input = $('input[name=' + prop + ']');
                $input.val(storage[prop]);
            }
        }
        if (!localStorage['product_price']) {
            var add_list_price = {}
            localStorage.setItem('product_price', JSON.stringify(add_list_price));
        }
        if (localStorage['product_price']) {
            var prop_price
            var storage_price = JSON.parse(localStorage['product_price'])
            for (prop_price in storage_price) {
                var $input_price = $('input[id=' + prop_price + ']');
                $input_price.val(storage_price[prop_price]).change()
            }
        }

        /**/
        $("a#list_del").on('click', function() {
            var conform = confirm("Are You sure You want to Delete this list?");
            if (conform == true) {
                var url = "/customdelete?id=" + $(this).attr('value')
                window.location.href = url
            }
        });
        /*This event will submit the form on button click*/
        $("a#biztech__quick_order_add_to_cart").on('click', function() {
            ajax.jsonRpc('/custom/add', 'call', {
                'add_cart': localStorage
            }).then(function(data) {
                if (data = 'True') {
                    localStorage.clear();
                    var url_cart = '/shop/cart'
                    window.location.href = url_cart
                }
            });
        });

        /*This event will use to submit form on model button click to create list*/
        $("#biztech__quick_order_create_list").click(function() {
            var list_name = $('input[name="listname"]').attr("value")
            if (list_name) {
                ajax.jsonRpc('/createlist', 'call', {
                        'create_name': list_name
                    })
                    .then(function(data) {
                        if (data = 'false') {
                            alert("please provide unique list name");
                        }
                    })
            } else {
                alert("please provide list name");
            }
        });

        /*This event will redirect user to his or her quick order list*/
        $("a#biztech__quick_order_show_list").on('click', function() {
            var list_id = $('input[name="listid"]').attr("value")
            var url_delete_item = '/quickorder?id=' + list_id
            window.location.href = url_delete_item
        });

        /*This event will Add new product to current list*/
        $("input#edit_add_list").on('click', function() {
            var prod = []
            var list_id = $('input[name="listid"]').attr("value")
            if (this.checked) {
                var key_prod = $(this).attr('name')
                var value_prod = $(this).attr('value');
                if (key_prod in prod) {
                    alert("sorry")
                } else {

                    $('<li class="new_add" id="' + key_prod + '" name="' + value_prod + '"><span>' + value_prod + '</span><a id="clear">X</a></li>').appendTo("ul#selected_products")

                }
                prod.push(key_prod);
                ajax.jsonRpc('/delete/item', 'call', {
                        'edit_prod': prod,
                        'listid': list_id
                    })
                    .then(function(data) {
                        if (data = 'true') {
                            window.location.href = window.location.href
                        }
                    })


            }
        });

        /*This event will delete product from current list*/
        $("a#list_item_del").on("click", function() {
            $(this).closest('li').addClass('strikke')
            var delete_prod = []
            var list_id = $('input[name="listid"]').attr("value")
            delete_prod.push($(this).attr('value'));
            ajax.jsonRpc('/delete/item', 'call', {
                    'deletelist': delete_prod,
                    'listid': list_id
                })
                .then(function(data) {
                    if (data = 'false') {
                        var list_obj = $('input[name="list_obj"]').attr("value")
                        var url = "/quickorder/" + list_obj
                        window.location.href = url
                    }
                })
        });

        /*This event will delete product from current list*/
        $("a#list_all_item_del").on("click", function() {
            var delete_all = []
            var list_id = $('input[name="listid"]').attr("value")
            delete_all.push($(this).attr('value'));
            ajax.jsonRpc('/delete/item', 'call', {
                    'delete_all': delete_all,
                    'listid': list_id
                })
                .then(function(data) {
                    if (data = 'false') {
                        var list_obj = $('input[name="list_obj"]').attr("value")
                        var url = "/quickorder/" + list_obj
                        window.location.href = url
                    }
                })
        });

        /*Quantity Spinner*/
        $('input#js_quantity_biztech').on('change', function() {
            var prod_value = $(this).val();
            var prod_id = $(this).attr('name');
            var old_products = JSON.parse(localStorage['product_list']);
            old_products[prod_id] = prod_value;
            localStorage.setItem('product_list', JSON.stringify(old_products));
            var old_price = JSON.parse(localStorage['product_price']);
            ajax.jsonRpc('/quickorder/price_calculate', 'call', {
                'price_count_id': prod_id,
                'prodcount': prod_value
            }).then(function(data) {
                $('input[id=' + prod_id + ']').val(data).change()
                old_price[prod_id] = data
                localStorage.setItem('product_price', JSON.stringify(old_price))
            })
        });

        $('a.biztech_cart').on('click', function(ev) {
            var add_prod = $('#add_to_cart_list').attr('value')
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var $input = $link.parent().parent().find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + parseFloat($input.val(), 10);
            $input.val(quantity > min ? (quantity < max ? quantity : max) : min);
            $('input[name="' + $input.attr("name") + '"]').val(quantity > min ? (quantity < max ? quantity : max) : min);
            $input.change();
            var name = $input.attr('name')
            var old__cartproducts = JSON.parse(localStorage['product_list'])
            old__cartproducts[name] = quantity
            localStorage.setItem('product_list', JSON.stringify(old__cartproducts));

        });


        /* search bar */
        $("a#btn_custom_search_editlist").on("click", function() {
            $(this).closest("form").submit();
        });
        $("a#btn_custom_search_quickorder").on("click", function() {
            $(this).closest("form").submit();
        });
        $(document).on("keypress", ".search-query", function(e) {
            if (e.which == 13) {
                $(this).closest("form").submit();
            }
        });


        /* this will enable desable drop down for list at product page*/
        $("input#add_to_list_product").on('click', function() {

            if (this.checked) {
                $("div#custom_list_div").removeClass('cutom_div_list')
                $("div#alert").addClass('cutom_div_list')
            } else {
                $("div#custom_list_div").addClass('cutom_div_list')
            }
        });

        /* this will Add item on selected list from product page*/
        $("ul#list_custom li a").click(function() {
            var product_id = $("input[name='product_id']").attr("value");
            var prod = []
            var list_id = $(this).attr('value');
            prod.push(product_id)
            ajax.jsonRpc('/delete/item', 'call', {
                    'edit_custom': prod,
                    'listid': list_id
                })
                .then(function(data) {
                    if (data = 'false') {
                        $("div#custom_list_div").addClass('cutom_div_list');
                        $("div#alert").removeClass('cutom_div_list');
                    }
                })

        });


        /*This event will Add variant of product to current list*/
        $("input#edit_add_allto_list").on("click", function() {
            var add_all = []
            var list_id = $('input[name="listid"]').attr("value")
            add_all.push($(this).attr('name'));
            ajax.jsonRpc('/delete/item', 'call', {
                    'add_all': add_all,
                    'listid': list_id
                })
                .then(function(data) {
                    if (data = 'false') {
                        window.location.href = window.location.href
                    }
                })

        });

        $("a#add_to_list_product_btn").on('click', function() {
            ajax.jsonRpc('/user/login/validation', 'call', {}).then(function(data) {

                $("div#custom_list_div").toggleClass('cutom_div_list');

            })

        })

    });

    $(document).ready(function() {
        var tabels_issue = Array();
        var maxHeight = 0;
        jQuery(".table-issue").each(function(index, ele) {
            tabels_issue.push(ele);
            maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
        });
        jQuery(".table-issue").each(function(index, ele) {
            $(this).height(maxHeight);
        });
    });
}); 