class ModalDialog {
    /**
     * 
     * @param {*} modal_dialog_id str
     * @param {*} aOption array of dict {option:str, text:str, classname:str}
     * @param {*} text str 
     */
    constructor(modal_dialog_id, aOption, text='') {
        console.log('obj ModalDialog', modal_dialog_id)
        this.modal_dialog_id = modal_dialog_id;
        this.aOption = aOption;
        this.text = text;
        this.item_id = null;
        this.set_text();
        this._create_buttoms();
    }

    set_text() {
        document.querySelector(`#${this.modal_dialog_id}_text`).innerHTML = this.text;
    }

    _create_buttoms() {
        this.aOption.forEach(element => {
            let btn;
            btn = document.createElement("BUTTON");
            btn.innerHTML = element.text;
            btn.className = element.classname;
            btn.onclick = () => { 
                _action_modal_dialog(this.modal_dialog_id, element.option);
            }
            document.querySelector(`#${this.modal_dialog_id}__body__options`).appendChild(btn);
        });
    }
}