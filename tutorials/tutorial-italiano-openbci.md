#####

##### TUTORIAL PER L&#39;OPERATORE DEL VIDEO FEEDBACK

#####

Il Neurofeedback (NF) è un tipo di controllo a circuito chiuso che sfrutta la registrazione di un segnale elettroencefalografico, per produrre un segnale sonoro e/o visivo da somministrare al paziente. In questo modo il paziente impara ad influenzare l&#39;attività cerebrale autoregolamentandola. I segnali acustici e visivi sono dunque utilizzati come avvertimento per adottare strategie di controllo ed imparare a modulare volontariamente i propri ritmi sensori-motori. A seconda della prevalenza dell&#39;handicap motorio, si deciderà se effettuare il trattamento di NF per migliorare la mobilità della mano destra, sinistra o quella degli arti inferiori.

**TUTORIAL TECHNICO PER OPERATORE**

1. Avviare **Open BCI Electron Hub**

1. Iniziare con **OpenBci\_GUI** (in apertura si avvia la schermata che consente di impostare i canali, questa va modificata solo nel caso in cui si deve modificare il montaggio: per cambiare ad esempio i nomi di elettrodi); se non ci sono le modifiche da fare clicca sul **Esegui** e a questo punto inizia **OpenBci**.

![](RackMultipart20200522-4-4jvq96_html_61e645005f2cf2af.jpg)

Fig. 1 La finestra di OpenBCI\_GUI

3. Cliccare su **Start System** dal System Control Panel, e successivamente su **Start Data Stream** (questo consente di registrare il segnale dagli elettrodi scelti). Si possono cambiare alcune impostazioni nella visualizzazione del segnale, come anche i filtri.

![](RackMultipart20200522-4-4jvq96_html_c29eca980e758d81.jpg)

Fig. 2 Il panello di controllo di OpenBCI

A questo punto, è necessario abbassare le impedenze degli elettrodi selezionati (per controllare il valore delle Impedenze cliccare sul simbolo OHM a Dx del nome del canale, e così s visualizza il valore delle impedenze. Il valore deve essere inferiore di 5, una volta ragiunto il valore più basso possibile uscire dalla funzione di impedenze).

![](RackMultipart20200522-4-4jvq96_html_5cc52eb859797e52.jpg)

Fig. 3 La schermata di impedenze per gli elettrodi selezionati

1. Successivamente, si deve avviare **MOTOR IMAGERY WIZARD**

Questa applicazione ha diverse opzioni di scelta dei parametri:

- Cliccando su **RUN** si crea il collegamento con

- **OpenVibe Acquisition Server** e andare sulla tendina di Driver e selezionare **LabStreamingLAyer (LSL)**

- **Sample count sent per block deve essere impostato a 8**

- cliccare sul **CONNECT** , dopo circa 1 secondo

- compare l&#39;opzione del **PLAY** e quindi cliccare su questo pulsante, controllare che ci sia il passaggio dell&#39;informazione sulla barra di sotto (la barra diventa di colore verde)

![](RackMultipart20200522-4-4jvq96_html_960f9c47d96a1d7c.jpg)

Fig. 4 La finestra iniziale di Motor Imagery Wizard

![](RackMultipart20200522-4-4jvq96_html_14e8dec0bd4dd69b.jpg)

**Fig. 5** La finestra OpenVibe Acuisition Server con i parametri da impostare per creare il collegamento tra OpenVibe e OpneBCI

1. Cliccando su comando **NEXT** in basso a destra si ottiene la possibilità di impostare:

- tutti i parametri della SESSIONE corrente,
- informazioni del paziente,
- tipologia di riabilitazione prevista per paziente la quale va scelta in base al deficit motorio di ciascun paziente, e può riguardare una delle tre opzioni:

- Acquisition\_Mano Dx
- Acquisition\_Mano Sx
- Acquisition\_Piedi

Dopo aver inserito tutte le informazioni relative al paziente, cliccare su **NEXT**

![](RackMultipart20200522-4-4jvq96_html_a3acf000fd52aa54.jpg)

**Fig. 6.** La finestra di parametri del paziente

1. A questo livello si trovano le informazioni relative a tutte le fasi che devono essere effettuate in ogni singola sessione.

![](RackMultipart20200522-4-4jvq96_html_30d52bfe91fa02ba.jpg)

**Fig. 7** La finestra relativa agli step di Neurofeedback

**STEP 1: ACQUISITION**

Questo step è attinente alla fase di registrazione del segnale EEG associato alla immaginazione del movimento. È fondamentale per la buona riuscita del training che questa fase sia performata in modo rigoroso!

Una volta determinato lo scenario specifico per il paziente, fare **PLAY** (per visualizzare lo scenario sullo schermo aggiuntivo è necessario spostare la finestra dello scenario sullo schermo aggiuntivo, solo a questo punto si può ottenere lo sdoppiamento delle finestre su più monitor).

![](RackMultipart20200522-4-4jvq96_html_488f4e6fcc4403de.jpg)

**IMPORTANTE:** la sessione di acquisizione è composta da un totale di 160 trials, 80 per l&#39;immaginazione del movimento dell&#39;arto e restanti 80 per la condizione di relax. Le istruzioni per i pazienti (vedi sezione 2xxxx).

È necessario avviare le pause ogni 8 min circa. Le pause vanno impostate manualmente dal operatore e devono avvenire nel momento specifico della registrazione, ovvero tra una prova ed un&#39;altra. La durata delle pause è di circa 1-2 minuti. Per avviare la pausa, cliccare sul pulsante specifico, facendo attenzione a non selezionare il pulsante di STOP (questo potrebbe comportare la perdita dei dati registrati fino a questo punto).

Una volta terminata la registrazione, lo scenario si ferma da solo. A questo punto, dal panello di scelta iniziale (Menu GENERALE), scegliere lo step successivo:

**STEP 2 - TRAINING**

Questa è la fase di elaborazione del segnale EEG registrato nella fase precedente. Devono essere individuati i cambiamenti nelle frequenze e nelle ampiezze che si verificano durante immaginazione del movimento. Per questo motivo l&#39;operatore deve effettuare alcune operazioni di stima di accuratezza della seduta di training. Per questo devono essere individuate le frequenze che offrono i livelli più alti di accuratezza stimata.

All&#39;interno di questo livello, si possono trovare i scenari con seguenti nomi:

- Training\_Mano\_Dx
- Training\_Mano\_Sx
- Training\_Piedi

Nello scenario sul quale si sta lavorando, devono essere modificati dei parametri nel box di **FREQUENZE:**

![](RackMultipart20200522-4-4jvq96_html_b2f56a4bc184eac6.jpg)

Cliccando 2 volte sul box Frequenze, si apre la finestra di configurazione in qui di base sono inserite le frequenze comprese tra 8-30 Hz. Queste frequenze possono (avvolte devono) essere personalizzate tra i pazienti. Inoltre, le frequenze possono variare tra una sessione ed l&#39;altra all&#39;interno dello stesso paziente! È importante ricordare di controllare all&#39;inizio di ogni nuova sessione le frequenze che devono essere impostate e/o cambiate per la sessione corrente. Come prima scelta delle frequenze per il calcolo di accuratezze, si consiglia di impostare le frequenze di base alle seguenti voci:

**LOW CUT Frequency (Hz)**: 8 Hz

**HIGH CUT Frequency (Hz):** 30 Hz

e cliccare il comando **PLAY** in alto.

---------------Inserire immagine-------------

Il messaggio del risultato del calcolo appare in automatico nella barra dei messaggi in basso a sinistra per visualizzarlo cliccare sul segno + (più) in basso a sinistra sulla stessa barra, a questo punto va controllato l&#39;esito della classificazione. Il valore di Cross\_Validation dovrebbe essere = \&gt; 60.

Se questo valore dovesse essere più basso, è necessario riavviare l&#39;analisi, cambiando i valori delle frequenze, impostando ad esempio 16-24Hz, (controllare il risultato della Cross\_Validation) e infine, avviare l&#39;analisi 13-30Hz, finalmente si può provare 8-12Hz. È necessario trovare il risultato di Cross\_Validation con il valore più alto. Ripetendo le analisi, vengono creati automaticamente tutti i files di training, in sequenza cronologica. Questo significa, che per l&#39;esempio riportato di sopra, prima verrà creato il file:

Training (con le frequenze tra 8-30Hz),

Training2 (per le frequenze comprese tra 16-24Hz),

Training3 (per le frequenze comprese tra 13-30Hz),

Training4 (per le frequenze comprese tra 8-12Hz).

ATTUALEMENTE SE SI RIPERE Più VOLTE IL CLASSIFICAT

ORE, VIENE SALVATO SOLAMENTE L&#39;ULTIMO (MODIFICA IN CORSO).

Nel caso in qui non si riesce ottenere il risultato di Cross\_Validation =\&gt; 60, si deve scegliere il file di training che ha prodotto il valore più alto. Questo file va impostato nello step successivo, il quale va selezionato dal Menu Principale.

**STEP 3.1 - GRAZ**

Lo scenario di Graz serve per testare se con le frequenze selezionate, il paziente può effettivamente controllare il software. Per questo, il file di Training ottenuto nella fase precedente, va impostato nello scenario di GRAZ. Cliccando sul box:

**FILE DI TRAINING** , si apre il percorso della cartella all&#39;interno della quale si trovano tutti i file di trainig eseguiti per questa specifica sessione, selezionare quindi il file di training desiderato.

Inserire, inoltre, lo stesso range di frequenze nel box di **FREQUENZE**. Cliccare sul **APPLAY** (altrimenti le modifiche non verranno salvate).

Il compito del paziente in questa fase…

![](RackMultipart20200522-4-4jvq96_html_654f8f46b164f3.jpg)

Avviare lo scenario premendo sul **PLAY**

**STEP 3.2 - ONLINE**

Lo scenario di Videofeedback serve per….

Anche in questo scenario, va impostato il file di Training ottenuto nella fase precedente, cliccando sul box:

**FILE DI TRAINING** , si apre il percorso della cartella all&#39;interno della quale si trovano tutti i file di trainig eseguiti per questa specifica sessione, selezionare quindi il file di training desiderato.

Inserire, inoltre, lo stesso range di frequenze nel box di frequenze. Cliccare sul **APPLAY** (altrimenti le modifiche non verranno salvate).

Infine, cliccare sul commando **PLAY** , compare la matrice con 2 quadrati colorati all&#39;interno dei quali si dovrebbero vedere i valori che cambiano (questo è il segno che il collegamento funziona) e a quel punto avvia il Videofeedback ()

![](RackMultipart20200522-4-4jvq96_html_3b67230b15f32072.jpg)

![](RackMultipart20200522-4-4jvq96_html_3c8b6aa56dec05ef.jpg)

