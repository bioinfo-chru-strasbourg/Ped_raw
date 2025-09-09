<template>
  <alert :message=message v-if="showMessage"></alert>
  <errorMessage :message=message v-if="showError"></errorMessage>
  <nav class="nav d-flex justify-content-center" style="margin-bottom: 2rem;">

    <Dropdown v-model="selectedBase" :options="bases" placeholder="Search for or select an existing pedigree database"
      class="w-full md:w-14rem" style="min-width: 40%; margin-right: 2rem;" @change="selectBase()" />
    <Button label="Create new database" icon="pi pi-plus" severity="success" size="small" @click="DialogCreateDB()"
      raised />

  </nav>
  <div>
    <div class="card">
      <Toolbar class="mb-4">
        <template #start>
          <span
            v-tooltip.right="{ value: `<h6> Use this button when you have selected a database if you want to add a row. Don't forget to save your changes. </h6>`, escape: true, class: 'custom-error' }">
            <Button class="m-1" label="Add" icon="pi pi-plus" severity="success" @click="pedDialog = true"
              :disabled="!isBaseSelected" /> </span>
          <span
            v-tooltip.bottom="{ value: `<h6> Select rows and use this button to delete them. Don't forget to save your changes. </h6>`, escape: true, class: 'custom-error' }">
            <Button class="m-1" label="Delete" icon="pi pi-trash" severity="danger" @click="deletePedsDialog = true"
              :disabled="!selectedPeds || !selectedPeds.length" /></span>
        </template>
        <template #center>
          <span
            v-tooltip.bottom="{ value: `<h6> Use this button when you have made changes to a database to save them. </h6>`, escape: true, class: 'custom-error' }">
            <Button class="m-1" v-if="unsavedChanges == false" label="Saved." icon="pi pi-check-square" severity="success"
              size="large" disabled @click="confirmSaveDialog = true" />
            <Button class="m-1" v-if="unsavedChanges" label="Save your changes to database" icon="pi pi-save
" severity="warning" size="large" @click="confirmSaveDialog = true" raised />
          </span>
        </template>
        <template #end>
          <span
            v-tooltip.bottom="{ value: `<h6> Use this button when you have selected a database to import data into it. <br> <strong> More information is available in the 'Documentation' page. </strong> </h6>`, escape: true, class: 'custom-error' }">
            <FileUpload mode="basic" accept=".csv,.tsv,.xlsx,.ped" :maxFileSize="1000000" label="Import"
              chooseLabel="Import" class="m-1" :disabled="!isBaseSelected" :auto="true" url="localhost:4280/upload"
              customUpload @uploader="onUpload" />
          </span>
          <span
            v-tooltip.left="{ value: `<h6> Use this button when you have selected a database to download its data. </h6>`, escape: true, class: 'custom-error' }">

            <Button class="m-1" label="Download" severity="help" icon="pi pi-download" @click="downloadDialog = true"
              :disabled="!isBaseSelected" />

          </span>
        </template>
      </Toolbar>

      <DataTable ref="dt" :value="peds" v-model:editingRows="editingRows" v-model:selection="selectedPeds"
        v-model:filters="filters" dataKey="id" editMode="row" filterDisplay="row" @row-edit-save="onRowEditSave"
        tableClass="editable-cells-table" :paginator="true" :rows="10" showGridlines
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLinkLastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5, 10, 25, 50]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} peds">

        <Column selectionMode="multiple" style="width: 2rem" :exportable="false"></Column>
        <Column field="id" header="Patient ID" sortable style="min-width: 9rem;">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" v-tooltip.top.focus="'Hit any key to filter'" type="text"
              @keydown="filterCallback()" class="p-column-filter" placeholder="Search for an ID" style="width: 9rem;" />
          </template>
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" required="true" style="min-width: 8rem; max-width: 10rem;" />
          </template>
        </Column>
        <Column field="famID" header="Family ID" sortable style="min-width: 8rem;">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" v-tooltip.top.focus="'Hit any key to filter'" type="text"
              @keydown="filterCallback()" class="p-column-filter" placeholder="Search for an ID" style="width: 9rem;" />
          </template>
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" required="true" style="min-width: 8rem; max-width: 10rem;" />
          </template>
        </Column>

        <Column field="paternalID" header="Paternal ID" sortable style="min-width: 7rem">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>


        </Column>
        <Column field="maternalID" header="Maternal ID" sortable style="min-width: 7rem">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>
        </Column>
        <Column field="sex" header="Sex" sortable style="min-width: 4rem">
          <template #editor="{ data, field }">
            <Dropdown v-model="data[field]" :options="sexes" style="width: 6rem" required="true" />
          </template>
        </Column>
        <Column field="phenotype" header="Phenotype" style="min-width: 7rem" sortable>
          <template #editor="{ data, field }">
            <Dropdown v-model="data[field]" :options="phenotypes" style="width: max-content" required="true" />
          </template>
        </Column>
        <Column field="alias" header="Aliases" sortable style="min-width: 7rem">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" style="width: 6rem" />
          </template>
        </Column>
        <Column field="HPOList" header="HPO List" sortable style="min-width: 11rem">
          <template #body="{ data, field }">
            <Chip v-for="hpo in data[field]">
              {{ hpo }}
            </Chip>
          </template>
          <template #editor="{ data, field }">
            <Chips id="HPOList" v-model="data[field]" rows="3" cols="20" separator="," style="width: 6rem" />
          </template>
        </Column>
        <Column field="starkTags" header="STARK Tags" sortable style="min-width: 11rem">
          <template #body="{ data, field }">
            <Chip v-for="starktag in data[field]" severity="success"> {{ starktag }} </Chip>
          </template>
          <template #editor="{ data, field }">
            <Chips id="starkTags" v-model="data[field]" rows="3" cols="20" separator="!" style="width: 6rem" />
          </template>
        </Column>
        <Column :exportable="false" :rowEditor="true" style="min-width: 5rem; max-width: 6rem"
          bodyStyle="text-align:center"></Column>
      </DataTable>
    </div>
  </div>

  <Dialog v-model:visible="pedDialog" :style="{ width: '50rem' }" header="Pedigree file form" :modal="true"
    class="p-fluid">
    <div class="field">
      <label for="id">Patient ID</label>
      <InputText id="id" v-model.trim="ped.id" required="true" autofocus
        :class="{ 'p-invalid': submitted && !ped.id | submitted && this.idDuplicate == true }" />
      <small class="p-error" v-if="submitted && !ped.id | submitted && this.idDuplicate == true">A unique ID is
        required.</small>
    </div>
    <div class="field">
      <label for="id">Family ID</label>
      <InputText id="famID" v-model.trim="ped.famID" autofocus />
    </div>

    <div class="field">
      <label for="paternalID">Paternal ID</label>
      <InputText id="paternalID" v-model="ped.paternalID" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="maternalID">Maternal ID</label>
      <InputText id="maternalID" v-model="ped.maternalID" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="sex">Sex</label>
      <SelectButton v-model="ped.sex" :options="sexes" aria-labelledby="basic" rows="3" cols="20" required="true" />
    </div>
    <div class="field">
      <label for="phenotype">Phenotype</label>
      <SelectButton v-model="ped.phenotype" :options="phenotypes" aria-labelledby="basic" rows="3" cols="20"
        required="true" />
    </div>
    <div class="field">
      <label for="alias">Alias</label>
      <InputText id="alias" v-model="ped.alias" rows="3" cols="20" />
    </div>
    <div class="field">
      <label for="HPOList">HPO List (tags separated by a comma ",")</label>
      <Chips id="HPOList" v-model="ped.HPOList" rows="3" cols="20" separator="," />
      <div class="field">
        <label for="starkTags">STARK Tags (tags separated by an exclamation point "!" )</label>
        <Chips id="starkTags" v-model="ped.starkTags" rows="3" cols="20" separator="!" />
      </div>
      <div>
        <Button label="Annuler" icon="pi pi-times" severity="danger" text @click="cancelAddTemp()" />
        <Button label="Continuer" icon="pi pi-check" type="submit" text @click="addPedTemp()" />
      </div>
    </div>
  </Dialog>

  <Dialog v-model:visible="deletePedsDialog" :style="{ width: '50rem' }" header="Confirmation" :modal="true">
    <div class="confirmation-content">
      <InlineMessage severity="warn" v-if="ped" style="font-size: 10rem;">
        Are you sure you want to delete the selected file(s)?
      </InlineMessage>
      <br /><br />
      <small>
        Your changes will not be saved until you press the "Save your changes"
        button.</small>
    </div>
    <template #footer>
      <Button label="Non" icon="pi pi-times" text @click="deletePedsDialog = false" />
      <Button label="Oui" icon="pi pi-check" text @click="deleteSelectedPeds" />
    </template>
  </Dialog>

  <Dialog v-model:visible="confirmSaveDialog" :style="{ width: '50rem' }" header="Confirmation" :modal="true">
    <div class="confirmation-content">
      <p id="saving">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        Are you sure you want to save all pedigree modifications in the <span style="color:red"> {{ manualSelectedBase }}
        </span> file ?
      </p>
    </div>
    <template #footer>
      <Button label="No" icon="pi pi-times" text @click="confirmSaveDialog = false" />
      <Button label="Yes" icon="pi pi-check" text @click="savePedsDef()" />
    </template>
  </Dialog>


  <Dialog v-model:visible="baseDialog" :style="{ width: '50rem' }" header="New database form" :modal="true"
    class="p-fluid">
    <InlineMessage severity="warn">You will need to refresh the page to access your new database.</InlineMessage>
    <div class="field">
      <label for="name">Database Name</label>
      <InputText v-model="selectedBase" required="true" autofocus
        :class="{ 'p-invalid': submitted && !ped.id | submitted && this.idDuplicate == true }" />
      <small class="p-error" v-if="submitted && !ped.id | submitted && this.idDuplicate == true">A unique database name is
        required.</small>
    </div>
    <template #footer>
      <Button label="Cancel" icon="pi pi-times" text @click="baseDialog = false" />
      <Button label="Confirm" icon="pi pi-check" text @click="confirmCreateDB()" />
    </template>
  </Dialog>


  <Dialog v-model:visible="dialogUnsaved" :style="{ width: '50rem' }" header="Changing database" :modal="true"
    class="p-fluid">
    <InlineMessage severity="warn"> You are leaving your database with unsaved changes. Are you sure you want to cancel
      your changes ? </InlineMessage>

    <Button label="Go back" icon="pi pi-times" text @click="cancelChoose()" />
    <Button label="Leave this base" icon="pi pi-check" text severity="warning" @click="chooseBase()" />

  </Dialog>

  <Dialog v-model:visible="downloadDialog" header="Download method" :modal="true" class="p-fluid"
    style="width: fit-content;">
    <div>
      <p>
        <InlineMessage severity="info"> Please choose what type of file do you want to download
          the
          data
          as. </InlineMessage>
        <br>
        <SelectButton v-model="typeFile" @change="downloadFile()" :options="downloadTypes" style="text-align: center;" />
      </p>{{ typeFile }}
    </div>
  </Dialog>
</template>



<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Error from './Error.vue';
import { ref } from 'vue';
import { isEqual } from 'lodash';
import { FilterMatchMode } from "primevue/api";
import { saveAs } from 'file-saver';
import { getBackendURL } from '@/common'




export default {
  data() {
    return {
      serverURL: getBackendURL(),
      peds: ref(),
      ped: ref({ "id": "", "famID": "", "paternalID": "", "maternalID": "", "sex": "Unknown", "phenotype": "Missing", "alias": "", "HPOList": [], "starkTags": [] }),
      originalTable: ref(false),
      originalPed: ref({}),
      unsavedChanges: ref(false),
      pedDialog: ref(false),
      deletePedsDialog: ref(false),
      confirmSaveDialog: ref(false),
      baseDialog: ref(false),
      dialogUnsaved: ref(false),
      confirmChange: ref(false),
      idDuplicate: ref(false),
      visible: ref(false),
      isBaseSelected: ref(false),
      editingRows: [],
      selectedPeds: ref(),
      selectedBase: ref(),
      manualSelectedBase: ref(),
      bases: ref([]),
      newData: ref(),
      dt: ref(),
      submitted: ref(false),
      message: '',
      sexes: ["M", "F", "Unknown"],
      phenotypes: ["Affected", "Unaffected", "Missing"],
      filters: ref({
        'id': { value: null, matchMode: FilterMatchMode.CONTAINS },
        'famID': { value: null, matchMode: FilterMatchMode.CONTAINS }
      }),
      showMessage: ref(false),
      showError: ref(false),
      string_save: "",
      downloadDialog: ref(false),
      downloadTypes: ["Ped file", "Advanced Ped file"],
      typeFile: '',
    };
  },
  components: {
    alert: Alert,
    errorMessage: Error,
  },
  methods: {
    onRowEditSave(event) {
      this.showError = false;
      this.submitted = true;
      let { newData, index } = event;
      console.log("new data after edit:", newData);
      this.getDuplicate(newData);
      if (newData.id != this.peds[index].id && this.idDuplicate) { // si l'id a change et qu'il existait deja
        this.message = "The ID you are trying to edit is already used. Every row needs to have a unique ID, please try again."
        this.showError = true;
      } else {
        this.peds[index] = newData;
        this.tablesChanged();
      }


    },
    getPeds() {
      this.showError = false;
      const path = this.serverURL + '/ped';
      axios.get(path, { withCredentials: true })
        .then((res) => {
          this.peds = res.data;
          console.log('peds gotten', this.peds);
          if (this.originalTable) {
            this.getOriginal();
            this.originalTable = false;
          }
        })
        .catch((error) => {
          console.error(error);
          this.message = "Error while getting the file data."
          this.showError = true;
        });

    },
    getBases() {
      const path = this.serverURL + '/files'
      axios.get(path, { withCredentials: true })
        .then((res) => {
          this.bases = res.data;
          console.log("get all the bases available:", this.bases);
        });
    },
    selectBase() {
      if (this.unsavedChanges) {
        this.dialogUnsaved = true;
      } else {
        this.chooseBase();
      }

    },
    chooseBase() {
      this.showError = false;
      this.unsavedChanges = false;
      this.dialogUnsaved = false;
      this.selectedPeds = [];
      this.isBaseSelected = true;
      this.manualSelectedBase = (' ' + this.selectedBase).slice(1); //deep copy
      const path = this.serverURL + '/files'
      axios.post(path, { "mybase": this.selectedBase }, { withCredentials: true })
        .then(() => {
          console.log("base chosen:", this.selectedBase);
        })
        .catch((error) => {
          console.log(error);
          this.message = "Error while changing base";
          this.showError = true;

        })
        .finally(() => {
          this.getPeds();
        });
      this.baseDialog = false;
    },

    confirmChangeBase() {
      this.confirmChange = true;
      chooseBase();
    },
    cancelChoose() {
      this.showMessage = false;
      this.dialogUnsaved = false;
      this.selectedBase = this.manualSelectedBase

    },
    DialogCreateDB() {
      this.message = false;
      this.baseDialog = true;
      this.selectedBase = null;
    },
    confirmCreateDB() {
      this.chooseBase();
      this.message = "Your new database has been created. Please refresh the website to access it.";
      this.showMessage = true;


    },
    getOriginal() {
      this.originalPed = JSON.parse(JSON.stringify(this.peds));
      console.log('original ped', this.originalPed);
      this.unsavedChanges = false;
    },
    savePedsDef() {
      this.showMessage = false;
      this.showError = false;
      const path = this.serverURL + '/ped';
      this.payload = JSON.parse(JSON.stringify(this.peds));
      console.log("payload (what will be saved)", this.payload);
      axios.post(path, this.payload, { withCredentials: true })
        .then(() => {
          this.originalTable = true;
          this.getPeds();
          console.log('Add complete !');
          this.confirmSaveDialog = false;
          this.getOriginal();
          this.unsavedChanges = false;
          this.message = " The file has been saved.";
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.confirmSaveDialog = false;
          this.message = "Error happened while saving peds";
          this.showError = true;
        });

    },
    cancelAddTemp() {
      this.pedDialog = false;
      this.ped = { 'id': "", 'alias': "", "paternalID": "", "maternalID": "", "sex": "Unknown", "phenotype": "Missing", "HPOList": [], "starkTags": [] };
      this.submitted = false;
    },
    getDuplicate(ped) {
      const listeID = [];
      for (let i of this.peds) {
        listeID.push(i.id);
      }
      this.idDuplicate = listeID.includes(ped.id);
    },
    addPedTemp() {
      this.showMessage = false;
      this.submitted = true;
      this.getDuplicate(this.ped)

      if (this.ped.id && !this.idDuplicate) {
        console.log("ped we want to add", this.ped);

        if (!this.ped.famID) {
          this.checkFamIDadd();
        }

        this.peds.push(JSON.parse(JSON.stringify(this.ped))); //copie dans peds (deep copy)
        this.pedDialog = false;
        this.ped = { 'id': "", 'alias': "", "paternalID": "", "maternalID": "", "sex": "Unknown", "phenotype": "Missing", "HPOList": [], "starkTags": [] };
        console.log("peds after the add", this.peds);
        this.tablesChanged();
        this.submitted = false;
        this.message = "Ped added ! Don't forget to save before leaving.";
        this.showMessage = true;

      }
    },
    checkFamIDadd() {
      let ListeFamID = new Array();
      let biggerfam = 0;
      for (let oneped of this.peds) {

        ListeFamID.push(oneped.famID)
        console.log('famIDs list', ListeFamID)
      }
      for (let fam of ListeFamID) {
        let famtemp = parseInt(fam.substring(3, 7));
        if (famtemp > biggerfam) {
          biggerfam = famtemp;
        }
      }
      let newfamNum = biggerfam + 1;
      let newfamLength = newfamNum.toString().length;
      if (newfamLength == 1) {
        console.log('1ere boucle');
        var newfamID = 'FAM' + '00' + newfamNum.toString();
        console.log('newfamid', newfamID)
      }
      else if (newfamLength == 2) {
        console.log('boucle 2');
        var newfamID = 'FAM' + '0' + newfamNum.toString();
      }
      else if (newfamLength == 3) {
        console.log('boucle 3')
        var newfamID = 'FAM' + newfamNum.toString();
      }
      else if (ListeFamID.length < 1) {
        var newfamID = 'FAM001'
      }
      console.log('newfamid', newfamID)
      this.ped.famID = newfamID

    },
    deleteSelectedPeds() {
      this.showMessage = false;
      this.peds = this.peds.filter(
        (val) => !this.selectedPeds.includes(val)
      );
      this.deletePedsDialog = false;
      this.selectedPeds = null;
      console.log('deleted');
      this.tablesChanged();
      this.message = "Ped removed ! Don't forget to save before leaving.";
      this.showMessage = true;
    },
    tablesChanged() {
      if (!isEqual(this.peds, this.originalPed)) {
        this.unsavedChanges = true;
      } else {
        this.unsavedChanges = false;
      }
    },
    onUpload(event) {
      this.showMessage = false;
      this.showError = false;
      console.log("event:", event)
      let fileUp = event.files[0];
      let formData = new FormData();
      formData.append('file', fileUp);
      console.log("fileup", fileUp);
      const path = this.serverURL + '/upload';
      axios.post(path, formData, { withCredentials: true })
        .then((res) => {
          console.log("fileup", fileUp);
          console.log("res data", res.data);
          if (typeof res.data === "string") {
            this.message = res.data;
            this.showError = true;
          } else {
            this.peds = res.data;
            this.unsavedChanges = true;
            this.message = " Import successful !";
            this.showMessage = true;
          }

        })
        .catch((error) => {
          console.log(error);
          this.message = "Import Error"
          this.showError = true;
        })
    },
    downloadFile() {
      this.showError = false;
      this.showMessage = false;
      const path = this.serverURL + "/download"
      let string_type = this.typeFile.substring(0, 3)

      axios.post(path, { "typefile": this.typeFile }, { withCredentials: true, responseType: 'blob' })
        .then((res) => {
          let data = res.data;
          saveAs(data, this.selectedBase + string_type + ".ped"); this.message = "The download of the '" + this.selectedBase + "' file has started.";
          this.showMessage = true;

        })
        .catch((error) => {
          console.log(error);
          this.message = "Export Error"
          this.showError = true;
        })
      this.typeFile = '';
    },

  },
  created() {
    this.originalTable = true;
    this.getBases();
    this.unsavedChanges = false;
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&display=swap');

html {
  font-size: 75%;
}

.p-button-label {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;

}
</style>
