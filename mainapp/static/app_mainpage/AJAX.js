<!-- Обработчик формы siteList -->
$(document).ready(function() {
        $('#sitelist_form').submit(function(e) {
          //отмена действия по умолчанию для кнопки submit
          e.preventDefault();
          let $form = $('sitelist_form'),
          sitelist_checkBox_myfin = $('#sitelist_form input[name=sitelist_checkBox_myfin]').is(':checked'),
          sitelist_checkBox_kucoin = $('#sitelist_form input[name=sitelist_checkBox_kucoin]').is(':checked'),
          sitelist_checkBox_coinbase = $('#sitelist_form input[name=sitelist_checkBox_coinbase]').is(':checked'),
          sitelist_checkBox_huobi = $('#sitelist_form input[name=sitelist_checkBox_huobi]').is(':checked');
          $.ajax({
            type: 'POST',
            url: '/api/v1/states/',
            //data:  $('#sitelist_form').serialize(),
            data: {
                'sitelist_checkBox_myfin': sitelist_checkBox_myfin,
                'sitelist_checkBox_kucoin': sitelist_checkBox_kucoin,
                'sitelist_checkBox_coinbase': sitelist_checkBox_coinbase,
                'sitelist_checkBox_huobi': sitelist_checkBox_huobi,
        },
            dataType: "json",
            headers: {'X-CSRFToken': "{{ csrf_token }}"},
            success: function (response) {
              //var dat = Object.entries(response.Success).join('\n');
              var dat = response.Success
              alert(dat);
              $('#u29_p').append('<span id="u29_s"></span>');
              $('#u29_s').text(dat);
              //$('#table-cell').text(Object.entries(response.mainpage_data).join('\n'))
              console.log('Пиздец!!')
            },
        });
      });
    });