from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import FileSystemStorage
from base.libs.template import Template
from base import config as PARAMS
from erdemo01.settings import BASE_DIR, MEDIA_ROOT
from base.business.bimport import BImport


@login_required(login_url='login')
def import_data(request):
    oTemplate = Template(None)
    oTemplate.template_title = f'{PARAMS.AppName} - Import'
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.import_form
    oTemplate.set_context()

    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            #print('myfile', myfile, myfile.name)
            fs = FileSystemStorage()
            #print('MEDIA_ROOT', MEDIA_ROOT)
            filename_url = os.path.join(MEDIA_ROOT,myfile.name)
            if fs.exists(filename_url):
            #    print('EXISTE')
                os.remove(filename_url)
            filename = fs.save(myfile.name, myfile)
            #uploaded_file_url = fs.url(filename)
            #excel_file = uploaded_file_url
            filename_url = os.path.join(MEDIA_ROOT,filename)
            
            print('root:', filename_url)

            oBImport = BImport(request)
            if not oBImport.getExcel(filename_url):
                print(oBImport.aMessage)
            else:
                oBImport.import_sheets()

            
            #empexceldata = pd.read_csv(BASE_DIR+excel_file,encoding='utf-8')

            # dColumn = {
            #     'producto' : {
            #         's_codigo' : 0,
            #         'unidad': 1,
            #         's_descripcion': 2,
            #         's_categoria': 3
            #     }
            # }

            
            # oExcelPd = ExcelPd(filename_url)
            # if oExcelPd.get_sheet('PRODUCTOS'):
            #     print('Rows:', oExcelPd.oSheet.rows)
            #     #for _, row in oExcelPd.oSheet.df.iterrows():
            #     #    print(row[0], row[1], row[2][:40])
                
            #     df_unidades = pd.DataFrame()
            #     df_unidades['unidad'] = oExcelPd.oSheet.df.iloc[:,dColumn['producto']['unidad']]
                
            #     # agrupar df_unidades por columna unidad (una unica fila pñor unidad)
            #     # groupby devuelve type obj Serie, pero con el reset_ibdex retornaun DF
            #     # reset_index agrega un indice y mueve las columnas
            #     df_unidades_group = df_unidades.groupby('unidad').size().reset_index()

            #     # reemplazar los valores en blanco por nan
            #     df_unidades_group['unidad'].replace('', np.nan, inplace=True)
                
            #     # eliminar filas que contengan valores nan
            #     df_unidades_group = df_unidades_group.dropna()
                
            #     # rename columnas 
            #     # la 1era columna paso a ser 'unidad', luego del reset_index)
            #     # la columna con el count es 0                
            #     df_unidades_group = df_unidades_group.rename(columns={0:'count'})

            #     # recorrer df_unidades_group
            #     for _, row in df_unidades_group.iterrows():
            #         print('row', row['unidad'], row['count'])
       
       
            # if oExcelPd.get_sheet('STOCK'):
            #     print('Rows:', oExcelPd.oSheet.rows)
            #     input()
            #     for _, row in oExcelPd.oSheet.df.iterrows():
            #         print(row[1], row[2], row[3][:40])
                
            #CODIGO  MATERIAL #

            #print(type(empexceldata))
            #dbframe = empexceldata
            #for dbframe in dbframe.itertuples():
                 
            #    print(dbframe)
 
            return render(request, oTemplate.template, context=oTemplate.context)
            
    except Exception as identifier:            
        print(identifier)
     

    return render(request, oTemplate.template, context=oTemplate.context)

