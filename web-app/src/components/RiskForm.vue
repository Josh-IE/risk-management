<template>
  <v-form>
    <v-layout
      row
      wrap
    >
      <v-flex md12>
        <p class="display-2 text-capitalize">{{riskModel.name}}</p>
      </v-flex>
      <v-flex md12>
        <p class="subheading">{{riskModel.description}}</p>
      </v-flex>
    </v-layout>
    <v-layout
      row
      wrap
    >
      <v-flex
        v-for="(field, index) in riskModel.fields"
        :key="field.id"
        xs12
        md6
      >
        <v-text-field
          v-if="['text', 'email', 'float', 'number', 'password', 'regex', 'url'].includes(field.field_type)"
          :key="index"
          v-model="formData['data'][field.slug]"
          :maxlength=field.max_length
          :counter=field.max_length
          :label="field.required ? field.name + '*' : field.name"
          :hint="field.help_text"
          required
          outline
          :type="field.field_type"
        ></v-text-field>
        <v-textarea
          v-else-if="field.field_type ==='textarea'"
          v-model="formData['data'][field.slug]"
          :counter="255"
          :hint="field.help_text"
          :label="field.required ? field.name + '*' : field.name"
          auto-grow
          outline
        ></v-textarea>
        <v-menu
          v-else-if="field.field_type ==='date'"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="290px"
        >
          <template #activator="{ on }">
            <v-text-field
              v-model="formData['data'][field.slug]"
              :label="field.required ? field.name + '*' : field.name"
              persistent-hint
              :hint="field.help_text"
              readonly
              outline
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="formData['data'][field.slug]">
            <v-spacer></v-spacer>
            <v-btn
              flat
              color="primary"
              @click="menu = false"
            >Cancel</v-btn>
            <v-btn
              flat
              color="primary"
              @click="$refs.menu.save(formData['data'][field.slug])"
            >OK</v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          v-else-if="field.field_type ==='time'"
          v-model="timeMenu"
          :close-on-content-click="false"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          max-width="290px"
          min-width="290px"
        >
          <template #activator="{ on }">
            <v-text-field
              v-model="formData['data'][field.slug]"
              :label="field.required ? field.name + '*' : field.name"
              persistent-hint
              :hint="field.help_text"
              readonly
              outline
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="timeMenu"
            v-model="formData['data'][field.slug]"
            format="24hr"
            full-width
            @click:minute="timeMenu=false"
          ></v-time-picker>
        </v-menu>
        <v-select
          v-if="field.field_type === 'select'"
          v-model="formData['data'][field.slug]"
          :items="field.choices"
          :label="field.required ? field.name + '*' : field.name"
          persistent-hint
          :hint="field.help_text"
          outline
        ></v-select>
        <v-select
          v-if="field.field_type === 'multiselect'"
          v-model="formData['data'][field.slug]"
          :items="field.choices"
          :label="field.required ? field.name + '*' : field.name"
          persistent-hint
          :hint="field.help_text"
          outline
          multiple
        ></v-select>
        <v-radio-group
          v-else-if="field.field_type ==='radio'"
          v-model="formData['data'][field.slug]"
          :label="field.required ? field.name + '*' : field.name"
          persistent-hint
          :hint="field.help_text"
        >
          <v-radio
            v-for="item in field.choices"
            :key="item"
            :label="item"
            :value="item"
          ></v-radio>
        </v-radio-group>
        <v-checkbox
          v-else-if="field.field_type ==='checkbox'"
          v-model="formData['data'][field.slug]"
          :label="field.name"
          persistent-hint
          :hint="field.help_text"
        ></v-checkbox>
        <v-switch
          v-else-if="field.field_type ==='switch'"
          v-model="formData['data'][field.slug]"
          :label="field.required ? field.name + '*' : field.name"
          persistent-hint
          :hint="field.help_text"
        ></v-switch>
        <v-combobox
          v-if="field.field_type === 'array'"
          v-model="formData['data'][field.slug]"
          :label="field.required ? field.name + '*' : field.name"
          :hint="field.help_text"
          multiple
          chips
          deletable-chips
          outline
        ></v-combobox>
        <div v-if="field.field_type === 'file'">
          <UploadBtn
            ref="button"
            :title="field.required ? field.name + ' *' : field.name"
            @file-update="(file)=> fileSelectedFunc(file, field.slug)"
            persistent-hint
            :hint="field.help_text"
          >
            <template slot="icon-left">
              <v-icon class="pr-2">cloud_upload
              </v-icon>
            </template>
          </UploadBtn>
          <button @click="$refs.button.clear()" />
        </div>
      </v-flex>
    </v-layout>
    <v-btn
      v-if="riskModel.fields.length"
      :class="[!riskModel.activated ? 'disabled-effect'  : '']"
      color="info"
      @click="handleSubmit"
      right
    >
      <v-icon>save</v-icon> {{riskModel.button}}
    </v-btn>
    <div class="text-xs-center">
      <v-dialog
        v-model="dialog"
        color="blue"
        width="500"
      >
        <v-card>
          <v-card-title
            primary-title
            :class="[submitSuccess ? 'blue' : 'red', 'headline']"
            :style="{color: 'white'}"
          >
            {{dialogTitle}}
          </v-card-title>
          <v-card-text v-if="this.submitSuccess">
            <p>{{riskModel.success_msg}}</p>
            <p>Form submission ID <span class="font-weight-medium">{{formSubmitID}}</span></p>
            <p>Risk model <span class="font-weight-medium text-capitalize">{{riskModel.id}}: {{riskModel.name}}</span></p>
            <p>
              View your Data here: <router-link :to="riskDataLink">Risk Data {{formSubmitID}}</router-link>
            </p>
          </v-card-text>
          <v-card-text v-else>
            <div
              v-for="(value, name) in formErrors"
              :key="name"
            >
              {{ name }}:
              <template v-for="(item, index) in value">
                <span :key="index">{{item}}</span>
              </template>
            </div>
          </v-card-text>
          <v-card-text v-if="this.info">
            <p>
              {{info}}
            </p>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              flat
              @click="dialog = false"
            >
              Dismiss
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-form>
</template>

<script>
import RiskModelService from '@/api-services/riskmodel.service'
import RiskDataService from '@/api-services/riskdata.service'
import UploadBtn from './UploadButton'
import objectToFormData from 'object-to-formdata'
export default {
  name: 'RiskForm',
  components: {
    UploadBtn
  },
  data () {
    return {
      riskModel: { 'fields': [] },
      formData: { 'data': {} },
      submitSuccess: false,
      dialog: false,
      dialogTitle: '',
      formSubmitID: '',
      formErrors: {},
      info: '',
      fileFieldPresent: false,
      menu: false,
      timeMenu: false
    }
  },
  computed: {
    riskDataLink () {
      return {
        name: 'risk-data',
        params: {
          id: this.formSubmitID
        }
      }
    }
  },
  mounted: function () {
    this.getRiskModel()
  },
  methods: {
    displaySuccessDialog: function (data) {
      this.submitSuccess = true
      this.dialog = true
      this.dialogTitle = 'Form Submit: Success'
      this.formSubmitID = data.form_submit
    },
    displayErrorDialog: function (err) {
      this.submitSuccess = false
      this.dialog = true
      this.dialogTitle = 'Form Submit: Error'
      this.formErrors = err
    },
    displayNotifyDialog: function (info) {
      this.submitSuccess = false
      this.dialog = true
      this.dialogTitle = 'Notification'
      this.info = 'This form is not active at the moment. Please contact Admin.'
    },
    getRiskModel: function () {
      let id = this.$route.params.id
      this.$emit('loader', true)
      RiskModelService.get(id)
        .then((response) => {
          console.log(response.data)
          this.riskModel = response.data
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
          this.buildFormData()
        })
        .catch(error => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          console.log(error.response.data)
        })
    },
    buildFormData: function () {
      this.riskModel['fields'].forEach((field) => {
        this.formData['data'][field.slug] = field.default
      })
      this.formData['risk_model'] = this.riskModel.id
      this.formData['risk_model_name'] = this.riskModel.name
    },
    postFormData: function () {
      this.$emit('loader', true)
      let formData = this.formData
      if (this.fileFieldPresent) {
        formData = objectToFormData(formData)
      }
      RiskDataService.create(formData)
        .then((response) => {
          console.log(response.data)
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
          this.displaySuccessDialog(response.data)
        })
        .catch(error => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          this.displayErrorDialog(error.response.data)
          console.log(error.response.data)
        })
    },
    handleSubmit: function () {
      if (this.riskModel.activated) {
        this.postFormData()
      } else {
        this.displayNotifyDialog()
      }
    },
    fileSelectedFunc: function (file, fieldSlug) {
      this.formData['data'][fieldSlug] = file
      if (file) {
        this.fileFieldPresent = true
      } else {
        this.fileFieldPresent = false
      }
    }
  }
}
</script>

<style scoped>
.disabled-effect {
  background-color: rgba(0, 0, 0, 0.12) !important;
}
</style>
