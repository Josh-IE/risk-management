// Risk Model UI component
<template>
  <v-form>
    <p class="display-2">{{title}}: <span class="text-capitalize">{{riskModel.name}}</span></p>
    <v-layout row>
      <v-flex
        xs12
        md6
      >
        <v-text-field
          v-model="riskModel.name"
          :counter="255"
          label="Name*"
          hint="Name/Title of the Risk Model"
          required
          outline
        ></v-text-field>
        <v-text-field
          v-model="riskModel.button"
          :counter="255"
          label="Button Text*"
          hint="Text on the Form's Submit Button"
          required
          outline
        ></v-text-field>
        <v-textarea
          v-model="riskModel.description"
          color="teal"
          label="Description"
          hint="Explanatory text about the Form"
          outline
        >
        </v-textarea>
      </v-flex>

      <v-flex
        xs12
        md6
      >
        <v-checkbox
          v-model="riskModel.activated"
          label="Active?"
          persistent-hint
          hint="Activate/Deactivate Form/Model. This controls the state of the form submit button."
          required
        ></v-checkbox>
        <v-textarea
          v-model="riskModel.success_msg"
          color="teal"
          label="Success Message"
          hint="Success message displayed after successful form submission"
          outline
        >
        </v-textarea>
      </v-flex>
    </v-layout>
    <Field
      v-for="(field, index) in riskModel.fields"
      :field="field"
      :index="index"
      :key="field.id"
      :fieldTypeChoices="fieldTypeChoices"
      @remove="remove(riskModel.fields, index)"
      @moveUp="moveUp(riskModel.fields, field)"
      @moveDown="moveDown(riskModel.fields, field)"
      ref="field"
    />
    <v-btn
      color="success"
      @click="addField"
    >
      <v-icon>add</v-icon> Add Field
    </v-btn>
    <v-btn
      color="info"
      @click="$emit('submit')"
      right
    >
      <v-icon>edit</v-icon> Save
    </v-btn>
  </v-form>
</template>
<script>
import RiskModelService from '@/api-services/riskmodel.service'
import Utils from '@/utils'
import Field from './Field'

export default {
  name: 'RiskModelUI',
  components: {
    Field
  },
  props: {
    riskModel: {
      type: Object,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      dialog: false,
      submitSuccess: false,
      dialogTitle: '',
      formErrors: {},
      fieldTypeChoices: []
    }
  },
  mounted: function () {
    this.getFieldTypeChoices()
  },
  methods: {
    displayErrorDialog: function (error) {
      this.submitSuccess = false
      this.dialog = true
      this.dialogTitle = 'Form Submit: Error'
      this.formErrors = error
    },
    getFieldTypeChoices: function () {
      RiskModelService.getFieldTypes().then((response) => {
        console.log(response.data)
        this.fieldTypeChoices = response.data
        this.$emit('loader', false)
        this.$emit('notifySuccess', true)
      }).catch((error) => {
        console.log(error.response.data)
        this.$emit('loader', false)
        this.$emit('notifySuccess', false)
      })
    },
    moveUp: function (array, element) {
      Utils.move(array, element, -1)
      Utils.refreshFieldOrder(array)
    },
    moveDown: function (array, element) {
      Utils.move(array, element, 1)
      Utils.refreshFieldOrder(array)
    },
    remove: function (array, index) {
      array.splice(index, 1)
      Utils.refreshFieldOrder(array)
    },
    addField: function () {
      this.riskModel['fields'].push({
        'name': null,
        'field_type': 'text',
        'default': null,
        'min_length': null,
        'max_length': null,
        'choices': null,
        'required': true,
        'help_text': null,
        'order': null
      })
      Utils.refreshFieldOrder(this.riskModel['fields'])
    }
  }
}
</script>
