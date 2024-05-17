class Form {
    /**
     * 
     * @param {*} aModal array of dict {id:str, id_btn_cancel:str}
     */
    constructor(aModal=null) {
        this.aModal = aModal;
    }

    init() {
        /**
         * Plantilla a usar en clase hija
         */

        this.set_events_form();
        if ( this.aModal ) {
         this.set_events_close_modal();
         this.set_events_modal();
        }
        this.init_data();
    }

    init_data() {
        /**
         * Plantilla a usar en clase hija
         */

        console.log('init data');
    }

    set_events_form() {
        /**
         * Plantilla a usar en clase hija
         */

        // eventos form principal
        // document.querySelector(`#${Venta.FORM.fields.cantidad}`).addEventListener(g_events.event_onkeyup, (e) => {
        //     controller(Lib.actions.action_events_form, e.target.id, e.type, e.key)
        // })

        console.log('set_events_form');
    }
    
    set_events_close_modal() {
        /**
         * Esto no se modifica. Requiere this.modals 
         */

        // set event al dar click fuera de un modal
        window.addEventListener('click', (e) => {
            this.aModal.forEach(modal => {
                if (e.target.id == modal.id) 
                    this.controller(Lib.actions.action_modal_close, modal.id);
            })
        })
    
        // set events close en modales al dar click en icono X o btn_cancel
        this.aModal.forEach(modal => {
            document.querySelector(`#${modal.id}_close`).addEventListener('click', () => {
                this.controller(Lib.actions.action_modal_close, modal.id);
            });
            if ( modal.btn_cancel_id != '' )
                document.querySelector(`#${modal.id}_${modal.id_btn_cancel}`).addEventListener('click', () => {
                    controller(Lib.actions.action_modal_close, modal.id);
                });
        })

        console.log('set_events_close_modal');
    }
    
    set_events_modal() {
        /**
         * Plantilla a usar en clase hija
         */
        
        // set events modal especfico
    
        // eventos modal_cobro
        // document.querySelector(`#${Venta.FORM.fields.metodo_pago_id}`).addEventListener(g_events.event_onchange, (e) => {
        //     controller(Venta.actions.action_events_modal_cobro, e.target.id, e.type);
        // });

        console.log('set_events_modal');
    }


    controller(action, ...parms) {
        let oController = Object;
        let data = { action: action };
        switch (action) {
    
            // ACCIONES QUE HARAN UN REQUEST
            /*
            case Venta.actions.action_save:
                let data_validate = funcionalida();
                // forma de validar si dict no está vacío
                if (Object.keys(data_validate).length) {
                    data = {
                        ...data, ...{
                            more_data: data_validate,
                        }
                    }
                    // newWindow = window.open("", "_blank");
                    oController = new Controller('/controller_venta', data, action_response_save_venta);
                    oController.fetch_action();
                }
                break;

            case Venta.actions.action_init_data_form:
                oController = new Controller('/controller_venta', data, action_response_init_data_form);
                oController.fetch_action();
                break;
            */
    
            //* ACCIONES EVENTOS form principal
            case Lib.actions.action_events_form: {
                let element_id = parms[0];
                let event_id = parms[1]; 
                let event_key = parms[2];
                console.log('action_event_form', element_id, event_id,event_key);
                
                this.action_events_form(element_id, event_id, event_key);
            }

            //* ACCIONES datalist
            case Lib.actions.action_datalist_selected: {
                let datalist_id = parms[0];
                let selected_id = parms[1];
                let selected_text = parms[2];
                switch (datalist_id) {
                    /*
                    case Venta.FORM.fields.cliente:
                        break;
                    */
                }
                break;
            }

            //* ACCIONES datagrid_items
            case Lib.actions.action_datagrid_action: {
                let datagrid_id = parms[0];
                let action_id = parms[1];
                let item_id = parms[2];
                this.action_datagrid_action(datagrid_id, action_id, item_id);
                break;
            }

            //* ACCIONES EVENTOS modal general
            case Lib.actions.action_modal_open: {
                let modal_id = parms[0];
                this.action_modal_open(parms);
                document.querySelector(`#${modal_id}`).style.display = 'block';
                break;
            }

            case Lib.actions.action_modal_close: {
                let modal_id = parms[0];
                document.querySelector(`#${modal_id}`).style.display = 'none';
                this.action_modal_close(modal_id);
                break;
            }

            //* ACCIONES MODAL_DIALOG
            case Lib.actions.action_modal_dialog: {
                let modal_dialog_id = parms[0];
                let option = parms[1];
                this.action_modal_dialog(modal_dialog_id, option);
                break;
            }

        }
    }

    action_modal_open(modal_id) {}    

    action_modal_close(modal_id) {}

    action_events_form(element_id, event_id) {}

    action_datagrid_action(datagrid_id, action_id, item_id) {}
    
    action_modal_dialog(modal_dialog_id, option) {}
}