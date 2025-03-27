import matplotlib.pyplot as plt,numpy as np,ftplib,getpass

#Convert cm to inch for matplotlib
def cm_to_inch(value):
    return value/2.54


def create_plot(x,y,title):

    # Figure Size
    fig, ax = plt.subplots(figsize =(cm_to_inch(40), cm_to_inch(20)),num=title)
    #Titel des Diagramms
    fig.suptitle(title)

    # Horizontal Bar Plot (Erstellt das Balkendiagramm) (barh erstellt horizontales Diagramm, bar verticales)
    ax.barh(x, y)

    # Remove axes splines () (Entfernt den Rahmen rund um das gesamte Diagramm)
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks, (Bindestriche nach dem Label und vor dem Balkendiagramm)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    # Add x, y gridlines (Erstellt die graue durchsichtige Tablelle)

    ax.grid(True, color='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
    # Show top values (Dreht die Reihenfolge der Balken um auf TOP --> DOWN, most used cipher --> last used cipher)
    ax.invert_yaxis()
    
    # Add annotation to bars (Fügt die Anzahl der Ciphers ans Ende des Balkens in jeder Reihe)
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')
    
    # # Add Plot Title
    # ax.set_title('Used TLS Ciphers',
    #              loc ='left', )
    
    

    #Kuemmert sich darum das die Labels nicht abgeschnitten dargestellt werden.
    plt.tight_layout()
    # Show Plot
    plt.show()


def download_logs():

    url=input_validation(str,"Please enter ESA Hostname for FTP Login (for example: esa01.test.at): ")
    username=input_validation(str,"Please enter ESA Admin Username: ")
    password=getpass.getpass("Please enter ESA Admin Password: ")
    
    path = '/mail_logs/'
    concatenated_logs=[]

    ftp = ftplib.FTP(url) 
    ftp.login(username, password) 
    ftp.cwd(path)
    filename_list = []
    #Get all information of files in current directory (mail_logs) and extract the file names into file_list 
    ftp.retrlines('LIST', lambda x: filename_list.append(x.split()))

    x=0
    while x < (len(filename_list)):
        #Download Files
        print(f"Downloading File: {filename_list[x][8]}")
        ftp.retrbinary("RETR " + filename_list[x][8], open(f"./logs/{filename_list[x][8]}", 'wb').write)
        #Read all downloaded file into one list, every newline is a new list item
        with open(f"./logs/{filename_list[x][8]}") as f:
            concatenated_logs += f.read().splitlines()
        x+=1
    ftp.quit()
    return concatenated_logs


def input_validation(input_datatype,input_text):
    
    input_var=input_datatype(input(input_text))    
    while (len(str(input_var)) <1): #len is only as string possible, so int is converted to str for this condition. The while loop ensures that the user types in the necesseary input (any character matches)
        input_var=input_datatype(input(input_text))
    return input_var
