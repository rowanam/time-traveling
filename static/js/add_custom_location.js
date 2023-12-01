// $(document).ready(function() {
//     $("#add-location").click(function() {
        
//     })
// })

// $('#add_more').click(function() {
//     cloneMore('div.table:last', 'service');
// });

// function cloneMore(selector, type) {
//     var newElement = $(selector).clone(true);
//     var total = $('#id_' + type + '-TOTAL_FORMS').val();
//     newElement.find(':input').each(function() {
//         var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
//         var id = 'id_' + name;
//         $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
//     });
//     newElement.find('label').each(function() {
//         var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
//         $(this).attr('for', newFor);
//     });
//     total++;
//     $('#id_' + type + '-TOTAL_FORMS').val(total);
//     $(selector).after(newElement);
// }

// var form_count = "{{formset.total_form_count}}";
// $('#add_form').click(function() {
//     form_count++;
//     var form = '{{formset.empty_form|escapejs}}'.replace(/__prefix__/g, form_count);
//     $('#forms').append(form)
//     $('#id_form-TOTAL_FORMS').val(form_count);
// });


$('#add_more').click(function() {
    console.log("Add more triggered");
    cloneMore('div.table:last', 'customtrips');
});


function cloneMore(selector, type) {
    console.log("Clone more function called");
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}