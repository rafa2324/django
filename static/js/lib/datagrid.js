/**
 * @class DataGrid
 * Se encarga de la funcionalidad de un datagrid.
 * Requiere libs.js, datagrid.css
 * Created by: Edgard Ramos (ismytv@gmail.com)
 */

 class DataGrid {
    actions_datagrid = {
        // action_delete: 'action_delete',
        // action_edit: 'action_edit',
        // action_refresh: 'action_refresh',
        // action_filter: 'action_filter',
        // action_filter_clear: 'action_filter_clear',
        action_pagination: 'action_pagination',
        action_pagination_previous: 'action_pagination_previous',
        action_pagination_next: 'action_pagination_next'
    }
    static mode_refresh = {
        online: 0,
        filter: 1,
        pagination: 2
    };

    /**
     * @constructror
    * @param {*} id             {string} id datagrid
    * @param {*} aData          {array of dict} data a mostrar
    * @param {*} aHeader        {array of array} glosas del header datagrid
    * @param {*} func_get_column {function} nombre de la función que devuelve lista con las valores de las columnas a mostrar por cada item de aData. La función recibe como parametro una fila de aData
    * @param {*} aAction         {array of dict} acciones  (default: ['Editar', 'Eliminar'])
    */
    constructor(id, aData, aHeader, func_get_column, aAction=null) {
        this.id = id;
        this.aData = aData;
        this.aHeader = aHeader;
        this.func_get_data_columns = func_get_column;
        this.aAction = aAction;

        // properties with default values
        this.aData_current = aData;
        this.show_header = true;
        this.show_footer = false;
        this.show_col_actions = true;
        this.ini_row = 1;
        this.current_page = 1;
        this.current_page_ini = 1; // pagina inicial de la actual relacion de paginas mostradas 
        this.max_rows_page = 10;
        this.max_pages = 10;    
        this.block_rows = 100;
        this.total_rows = 1; // total rows (sin paginacion)
        this.enabled_multiple_datagrid = false; // para redefinir valor prefijo nombre de clase col_*
        this.classname_column = 'col_';
        this._init_actions();
        
        // auxiliar's properties 
        this.div_id_header = this.id + '_header';
        this.div_id_detail = this.id + '_detail';
        this.div_id_footer = this.id + '_footer';
        this.div_id_pagination = this.id + '_pagination';
        this.div_id_pagination_buttons = this.id + '_pagination_buttons';
        this.div_id_pagination_text = this.id + '_pagination_text';


        this._create_divs();

    }

    _init_actions() {
        if ( this.aAction !== null )
            return;
        this.aAction = [
            {
                action:'edit',
                abrev:'Edit',
                icon:'edit'
            },
            {
                action:'delete',
                abrev:'Elim',
                icon:'delete'
            }
        ]
    }

    version() {
        console.log('version.2021');
    }

        

    /**
     * @metod @private
     * create_divs  Crea los elementos div para el datagrid dentro del div '#this.id'
     */
    _create_divs() {
        let datagrid_header, datagrid_detail, datagrid_footer;
        let datagrid_pagination, datagrid_pagination_buttons, datagrid_pagination_text;

        // header
        datagrid_header = document.createElement("DIV");
        datagrid_header.id = this.div_id_header;
        datagrid_header.classList.add('datagrid_header');
        // detail
        datagrid_detail = document.createElement("DIV");
        datagrid_detail.id = this.div_id_detail;
        datagrid_detail.classList.add('datagrid_detail');
        // footer
        if ( this.show_footer ) {
            datagrid_footer = document.createElement("DIV");
            datagrid_footer.id = this.div_id_footer;
            datagrid_footer.classList.add('datagrid_footer');
        }
        // pagination
        datagrid_pagination = document.createElement("DIV");
        datagrid_pagination.id = `${this.id}_pagination`;
        datagrid_pagination.classList.add('datagrid_pagination');
        
        // create elements
        document.querySelector(`#${this.id}`).appendChild(datagrid_header);
        document.querySelector(`#${this.id}`).appendChild(datagrid_detail);
        if ( this.show_footer ) {
            document.querySelector(`#${this.id}`).appendChild(datagrid_footer);
        }
        document.querySelector(`#${this.id}`).appendChild(datagrid_pagination);
        
        // pagination buttons
        datagrid_pagination_buttons = document.createElement("DIV");
        datagrid_pagination_buttons.id = this.div_id_pagination_buttons;
        datagrid_pagination_buttons.classList.add('datagrid_pagination__buttons');
        // pagination text
        datagrid_pagination_text = document.createElement("DIV");
        datagrid_pagination_text.id = this.div_id_pagination_text;
        datagrid_pagination_text.classList.add('datagrid_pagination__text');

        // create elements
        document.querySelector(`#${this.id}_pagination`).appendChild(datagrid_pagination_buttons);
        document.querySelector(`#${this.id}_pagination`).appendChild(datagrid_pagination_text);

        datagrid_pagination_buttons.addEventListener('click', (e)=>{
            this._controller(this.actions_datagrid.action_pagination, e.target);
        })
    }

    /**
     * @method @public
     * refresh Refresca el datagrid, incluye la paginación
     * @param {*} aData         {array dict} data a mostrar
     * @param {*} mode_refresh  {this.mode_refresh} data a mostrar
     */
     refresh(aData=this.aData, mode_refresh=DataGrid.mode_refresh.online) {  
        // redefine this.classname_col
        if ( this.enabled_multiple_datagrid ) {
            this.classname_column = `col_${this.id}_`
        }
        console.log('classname', this.classname_column)

        switch(mode_refresh) {
            case DataGrid.mode_refresh.online:
                this.aData = aData;
                this.aData_current = aData;
                break;
            case DataGrid.mode_refresh.filter:
                this.aData_current = aData;
                break;
            case DataGrid,mode_refresh.pagination:
                // this.aData_current es el mismo
                break;
        }
    
        let item;
        let html = '';

        if ( this.show_header ) this._show_grid_header();
        
        let range = this._get_range_rows_page();
        console.log('Range:', range)

        // muestra las filas que están en range
        for (let i=0; i<this.aData_current.length; i++) {
            if (i > range.pos_fin) break;

            if (!(i >= range.pos_ini && i <= range.pos_fin)) continue;

            item = this.aData_current[i];

            let striped = (i % 2 == 0) ? '' : 'grid__row__striped';
            html += `<div class="grid__row ${striped}">`;

            // FUNCIONALIDAD PERSONALIZADA
            // Llama a func_get_data_columns que devuelve un arrreglo con los datos a mostrar por cada columna
            // No incluye la columhna Acciones. 
            
            let aColumn = this.func_get_data_columns(item);
            aColumn.forEach((element, index) => {
                html += this._div_grid_column(element.data, `${this.classname_column}${index+1}`, `${element.class}`);
            })

            // Muestra la columna acciones a partir de this.aAction
            // Llamará a una función con nombre _datagrid_action() que debe existir en el js principal,
            // se envía como parametros: this.id, this.aAction[?].action, item.id
            if ( this.show_col_actions ) {
                html += `<div class="grid__col ${this.classname_column}${aColumn.length+1}">`;
                html += `<div class="grid__data">`;
                this.aAction.forEach((element) => {
                    html += ` <abbr title='${element.abrev}'>
                    <span class="material-icons " 
                    onclick="_datagrid_action('${this.id}', '${element.action}', ${item.id})">
                    ${element.icon}</span></abbr>`;
                })

                html += `</div>`;
               
                html += '</div>'; // grid__col
            }
            html += '</div>'; // grid__row

        }

        this._remove_pagination_buttons(this.div_id_pagination_buttons);
        
        // message si no hay datos
        if (this.aData_current.length == 0) {
            html += '<div class="grid__msg">No se encontraron datos</div>';
            document.querySelector(`#${this.div_id_pagination_text}`).innerHTML = ''
        }
        else {
            this._set_paginacion(this.aData_current.length);
            this._pagination_set_color_buttons(this.current_page);
            // document.querySelector(`#${this.div_id_pagination_text}`).innerHTML = `Registros del 
            //     ${range.pos_ini + 1} al ${range.pos_fin + 1} de un total de 
            //     ${aData.length} ` + ((aData.length>1)? 'registros.':'registro.' );
            document.querySelector(`#${this.div_id_pagination_text}`).innerHTML = `Registros del 
                ${range.pos_ini + this.ini_row} 
                al 
                ${range.pos_fin + this.ini_row } 
                de un total de 
                ${this.total_rows} ` + ((aData.length>1)? 'registros.':'registro.' );
        }

        // Actualizar elemento id=grid_detail
        // document.getElementById('grid_detail').innerHTML = html;
        document.querySelector(`#${this.div_id_detail}`).innerHTML = html;

    }

    

    /**
     * @method @private
     * Muestra el header a partir de this.aHeader
     * Si this.aHeader.lenght > 1 entonces se considera la tupla correspondiente segun tamaño de pantalla
     * La primera tupla tiene las etiquetas para pantallas grandes.
     * La segunda tupla tiene las etiqeutas para pantallas pequeñas.
     */
    _show_grid_header() {
        let html = '';
        let pos_label_size_screen = 0;
        
        pos_label_size_screen = (this.aHeader.length==1)? 0 : is_type_screen(g_min_size_screen.desktop)? 0 : 1;

        html += '<div class="grid__row grid__row__title">';
        this.aHeader[pos_label_size_screen].forEach((element, index) => {
            html += this._div_grid_column(element, `${this.classname_column}${index+1}`);
        });
        html += '</div>'; // grid__row   
        document.querySelector(`#${this.div_id_header}`).innerHTML = html;
    }

    /**
     * @method @private
     * Devuelve rango de filas a mostrar de this.aData para this.current_page.
     * this.current_page empieza en 1
     * @returns { pos_ini, pos_fin }
     */
    _get_range_rows_page() {
        console.log('current_page', this.current_page)
        let pos_ini = (this.current_page-1) * this.max_rows_page + 1;
        let pos_fin = pos_ini + this.max_rows_page - 1;
        pos_fin = (pos_fin > this.aData_current.length)? this.aData_current.length : pos_fin;
        return {
            pos_ini: pos_ini-1,
            pos_fin: pos_fin-1
        }
    }

    /**
     * @method @private
     * Devuelve codigo html para la columna a mostrar
     * @param {*} data                  {any} data a mostrar
     * @param {*} class_div_grid__col  {str} nombre de clase para la columna
     * @param {*} class_div_grid__data {str} nombre de clase para la data 
     * @returns {*} {str} codigo html
     */
    _div_grid_column(data, class_div_grid__col, class_div_grid__data='') {
        let html = '';
        html += `<div class="grid__col ${class_div_grid__col}">`;
        html += `<div class="grid__data ${class_div_grid__data}">${data}</div>`; 
        html += '</div>'; 
        return html;
    }

    /**
     * @method @private
     */
    _remove_pagination_buttons() {
        let x = document.querySelector(`#${this.div_id_pagination_buttons}`).querySelectorAll("BUTTON");
        // Array.from(x).forEach()
        for (let i = 0; i < x.length; i++) {
            x[i].remove();
        }
    }


    /**
     * @method @private
     * Crea los botones de la paginación
     * @param {*} rows {int} Numero de 
     */
    _set_paginacion(rows) {
        // calcula numero de botones de paginas a mostrar
        let num_pags = Math.ceil(rows/this.max_rows_page);
        //let page_fin = this.current_page_ini +this.max_pages-1;
        let page_fin = 1 + this.max_pages-1; 

        page_fin = (page_fin > num_pags)? num_pags : page_fin;
        console.log('ed_setpag_1', num_pags, page_fin)

        // crea boton Previo si es necesario
        //if ( this.current_page_ini > 1) {
        if ( this.ini_row > 1) {
            let btn = document.createElement("BUTTON");
            btn.innerHTML = `<<`;
            btn.id = `btn_page_previous`;
            // btn.onclick = () => { this._controller(this.actions_datagrid.action_pagination_previous); }
            document.querySelector(`#${this.div_id_pagination_buttons}`).appendChild(btn);
        }

        // crea botones por cada numero de página entre page_ini y page_fin 
        for (let i=0; i<num_pags; i++) {
            //if ( !(i>=this.current_page_ini-1 && i<=page_fin-1) ) continue;
            let btn = document.createElement("BUTTON");
            //btn.innerHTML = `${i+1}`;
            btn.innerHTML = `${i+this.current_page_ini}`;
            // btn.id = `btn_page_${i+1}`;
            btn.id = `${i+1}`;
            // btn.onclick = () => { this._controller(this.actions_datagrid.action_pagination, i+1); }
            document.querySelector(`#${this.div_id_pagination_buttons}`).appendChild(btn);
        }

        // crea boton Siguiente si es necesario
        //if ( page_fin < num_pags ) {
        if ( (this.ini_row + this.block_rows - 1) < this.total_rows) {
            let btn = document.createElement("BUTTON");
            btn.innerHTML = `>>`;
            btn.id = `btn_page_next`;
            // btn.onclick = () => { this._controller(this.actions_datagrid.action_pagination_next); }
            document.querySelector(`#${this.div_id_pagination_buttons}`).appendChild(btn);
        }
    }

    /**
     * @method @private
     * @param {*} action 
     * @param  {...any} parms 
     */
    _controller(action, ...parms) {
        let data = { action : action };
        switch (action) {
            case this.actions_datagrid.action_pagination:
                // accion al dar click en algun boton de paginación
                let target = parms[0];
                if ( target.tagName !== 'BUTTON' ) break;

                switch (target.id) {
                    case 'btn_page_previous':
                        //this.current_page_ini-= this.max_pages;
                        //this.current_page = this.current_page_ini;
                        //this.refresh(this.aData_current, DataGrid.mode_refresh.pagination, this.current_page_ini);
                        _datagrid_action(this.id, 'btn_page_prev', target.id)
                        break;
                        
                    case 'btn_page_next':
                        //this.current_page_ini+= this.max_pages;
                        //this.current_page = this.current_page_ini;
                        //this.refresh(this.aData_current, DataGrid.mode_refresh.pagination, this.current_page_ini);
                        _datagrid_action(this.id, 'btn_page_next', target.id)
                        break;

                    default:
                        // button con id = # de pagina
                        this.current_page = parseInt(target.id);
                        
                        this.refresh(this.aData_current, DataGrid.mode_refresh.pagination, this.current_page);
                        // console.log('action_pagination', parms[0], this.current_page);
                        break;
                }
                break;

        }

    }

    /**
     * @method @private
     */
    _pagination_set_color_buttons() {
        let buttons = document.querySelector(`#${this.div_id_pagination_buttons}`).querySelectorAll("button");
        buttons.forEach((button)=>{
            if ( button.id === `${this.current_page}` )
                button.classList.toggle('button_pagination_primary');
            else
                button.classList.toggle('button_pagination_secondary');
        })
    }

}