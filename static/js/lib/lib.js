const g_key = {
    enter: 'Enter',
    arrow_up: 'ArrowUp',
    arrow_down: 'ArrowDown'
}
const g_min_size_screen = {
    desktop: 768
}

const g_events = {
    event_onkeyup: 'keyup',
    event_onclick: 'click',
    event_onchange: 'change',
    event_input: 'input'
};
const g_actions_listview = {
    action_refresh: 'action_refresh',
    action_edit: 'action_edit',
    action_delete: 'action_delete',
    action_filter: 'action_filter',
    action_filter_clear: 'action_filter_clear',
}


class Lib {
    static actions = {
        // generales
        action_events_form: 'action_events_form',
        action_modal_open:  'action_modal_open',
        action_modal_close: 'action_modal_close',

        action_datalist_selected: 'action_datalist_selected',   //new
        action_datagrid_action: 'action_datagrid_action',        //new
        action_modal_dialog: 'action_modal_dialog'              //new
    }
    static id_btn_cancel_modal = 'btn_cancel'
    

    static set_select_tag(select_id, aOption) {
        /**
         * Agrega opciones a un elemento select(combo) y elimina las existentes
         * select_id    :   Identificador del tag elemento
         * aOptions     :   Array de dict con las opciones del select. Debe tener al 
         *                  menos las key: id, desc
         */

         let select = document.querySelector(`#${select_id}`);
         while (select.options.length ) 
             select.removeChild(select.options[0]);

         aOption.forEach((element, index) => {
             let option = document.createElement('option')
             option.value = element.id
             option.text = element.desc
             select.add(option);
         })
         if (aOption.length) 
            select.selectedIndex = 0;
    }
}


function action_redirect(url) {
    window.location.href = url;
}

function set_focus(element_id) {
    // $(`#${element_id}`).select();
    document.querySelector(`#${element_id}`).focus();
}

/**
 * Hace visible o no un element_id. 
 * @param element_id 
 * @param is_show : true or false
 * @param modo_display : block or flex
 */
function set_visible(element_id, is_show, modo_display = 'block') {
    document.querySelector(`#${element_id}`).style.display = (is_show) ? modo_display : 'none';
}

function convert_to_int(str) {
    str = (str.trim().length) ? str : '0';
    let number = parseInt(str);
    return isNaN(number) ? 0 : number;
}

function convert_to_float(str, dec=2) {
    let number = parseFloat(str);
    return isNaN(number) ? 0 : number;
}

/*
function get_datalist_atribute(input_id, datalist_id, atribute) {
    // Devueve el valor del atribute data-? de un datalist; caso contrario devuelve null
    let element_input = document.getElementById(input_id);
    let element_datalist = document.getElementById(datalist_id);
    let opSelected = element_datalist.querySelector(`[value="${element_input.value}"]`);
    let value = (opSelected != null) ? opSelected.getAttribute(atribute) : null;
    return value;
}
*/

/** Utilizado para mostrar un error personalizado en un input de un formulario
    retorna true (usado para indicar que se maneja un error)
*/
function show_msg_error_input(element_id, msg) {
    document.getElementById(element_id).innerHTML = msg;
    set_visible(element_id, true);
    return true;
}

function is_type_screen(min_size_screen) {
    return (screen.width >= min_size_screen) ? true : false;
}

/**
 * Devuele true si navegador es desktop. Pendiente revisar, por ahora lo determina por el min_size_screen.
 * Otra manera es con windows.navigator.userAgent, pero no lo recomiendan 100%
 */
function is_navigator_desktop() {
    return is_type_screen(g_min_size_screen.desktop);
}

/**
 * getCookie
 * Use for get csrftoken
 */
 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
