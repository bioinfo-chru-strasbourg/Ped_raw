<template >
  <div class="m-4">
    <Panel class="m-3" header="How to use" toggleable>
      <p class="m-2">
        Firstly, you will <u> need to choose which database to work with</u> : you can use the drop-down list to select an
        existing one, or create a new one using the button and then refresh the page to select it.
        <br>
        Then, you will be able to <u>import data</u> or <u>add a new row</u> manually, as well as to <u>delete</u> or
        <u>modify</u> existing ones. <strong> Each one of these changes will need to be saved or they will be
          lost.</strong>
      </p>
      <p class="m-2">

        <u>Imported files</u> will need to have a special structure. If they have a header: they are
        <strong>required</strong> to have at least
        one column for patient identification named 'id', 'Patient ID' or 'ID'. They can be TSV, CSV or XLSX . Here are
        the possible column names which
        will be used in this website. <br>
        They can have as many columns as you wish (as long as they have a header), they will simply be ignored if not in
        the
        following list :
      <ul>
        <li> <strong> "Family ID" column : </strong> "famID","Family ID" or "FAMID" </li>
        <li> <strong> "Patient ID" column : </strong> "id", "ID", "Patient ID" or "Individual ID"</li>
        <li> <strong> "Maternal ID" column : </strong> "maternalID", "Maternal ID", "mother" or "Mother" </li>
        <li> <strong> "Paternal ID" column :</strong> "paternalID", "Paternal ID", "father", "Father" </li>
        <li> <strong> "Sex" column :</strong> "sex", "Sex"
          <br><strong>Values accepted :</strong> <u>Female</u> :
          "F", "Female", "female", 2, "2". <u>Male</u> :
          "M", "Male", "male", 1, "1".
        </li>
        <li> <strong> "Phenotype" column :</strong> "phenotype, "Phenotype".
          <br> <strong>Values accepted :</strong> <u>Affected</u> :
          "Affected", "affected", 2, "yes", "Yes", "2". <u>Unaffected</u> : "Unaffected", "unaffected", "no", "No", 1,
          "1".
        </li>
        <li> <strong> "Aliases" column : </strong> "alias", "Alias" or "Aliases" </li>
        <li> <strong> "HPO List" column :</strong> "HPOList", "hpolist", "HPO List" </li>
        <li> <strong> "Stark Tags" column :</strong> "starkTags","Stark Tags", "starktags", "STARK Tags" or "tags" </li>
      </ul>
      </p>
      <p class="m-2">
        If they <strong>don't have a header</strong> : they will need to be at the Ped Format or our Advanced Ped Format.
        The separator in the .ped format is the tabulation.
        <br>
        <u>Ped format have 6 columns in this order</u> : "Family ID" , "Individual ID", "Paternal ID", "Maternal ID",
        "Sex"
        and
        "Phenotype".<br>
        <u>Advanced Ped format have 9 columns in this order</u> : "Family ID" , "Individual ID", "Paternal ID", "Maternal
        ID", "Sex",
        "Phenotype", "Alias", "HPO List" and "STARK Tags". <br><br>

        Moreover, you are able to <u>download</u> any of the files in those two formats.
      </p>
    </Panel>

    <Panel class="m-3" header="Pedigree files role" toggleable>
      <p class="m-2">
        Pedigree files document the structured descriptions of the familial relationship among samples in a study.
        <br>

        The files include information such as a unique identifier, their relationships, the individual's sex and their
        affected status. Our team added a list of HPO terms and tags for our Stark machine to assimilate further
        information.
        <br>

        Pedigree files are created based on information gathered from family members, medical records, or genetic testing,
        and they play a crucial role in understanding genetic inheritance patterns and conducting genetic analyses.
      </p>
    </Panel>
  </div>

  <div class="button">
    <small>Authors : &#160 &#160</small>
    <Button severity="warning" size="small" @click="getPingPong">{{ msg }}
    </Button>

  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { getBackendURL } from '@/common'

export default {
  name: 'Ping',
  data() {
    return {
      serverURL: getBackendURL(),
      msg: ref('MEDINA Solène !'),


    };
  },
  methods: {
    getPingPong() {
      const path = this.serverURL + '/ping';
      axios.post(path, { msg: this.msg }, { withCredentials: true })
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {

          console.error(error);
        });
    },

  },
  created() {

  },
};
</script>




<style>
.p-panel-header {
  font-size: 1.55rem;
}

.m-3 {
  width: 80%;

}

.m-2 {
  font-size: 1.2rem;
  text-indent: 3%;
}

.m-4 {
  min-width: 90%;
  width: 96%;
  max-width: 98%;
  position: relative;
  top: 10%;
  left: 10%;
}

.button {
  float: right;
  margin-bottom: 2%;
  margin-right: 2%;
  display: flex;
  align-items: center;
}

body {
  overflow-x: hidden;
}
</style>

