// Feedback UI Dialog  for RiskModel Create & Update
<template>
  <div class="text-xs-center">
    <v-dialog
      v-model="dialogObject.dialog"
      width="500"
    >
      <v-card>
        <v-card-title
          primary-title
          :class="[dialogObject.submitSuccess ? 'blue' : 'red', 'headline']"
          :style="{color: 'white'}"
        >
          {{dialogObject.dialogTitle}}
        </v-card-title>
        <v-card-text v-if="dialogObject.submitSuccess">
          <p>Risk Model ID <span class="font-weight-medium">{{dialogObject.data.id}}</span></p>
          <p>
            View its Form here: <router-link :to="riskFormLink">Risk Form {{dialogObject.data.id}}</router-link>
          </p>
          <p v-if="dialogObject.source === 'create'">
            Update the Model here: <router-link :to="riskModelLink">Edit Risk Model {{dialogObject.data.id}}</router-link>
          </p>
        </v-card-text>
        <v-card-text v-else>
          <div
            v-for="(value, fieldName) in dialogObject.formErrors"
            :key="fieldName"
          >
            <!-- if name is fields, nested field errors -->
            <template v-if="fieldName === 'fields'">
              <template v-for="(fieldObj, fieldIndex) in value">
                <template v-if="typeof(fieldObj) == 'string'">
                  {{fieldName}}: {{fieldObj}}
                </template>
                <template v-else-if="JSON.stringify(fieldObj) != '{}'">
                  Field[{{riskModel['fields'][fieldIndex].name}}]
                  <template v-for="(errors, subFieldName) in fieldObj">
                    <p
                      :key="subFieldName"
                      class="ml-4"
                    >{{subFieldName}}:
                      <template v-for="(item, index) in errors">
                        <span :key="index">{{item}}</span>
                      </template>
                    </p>
                  </template>
                </template>
              </template>
            </template>
            <template v-else>
              <!-- else list of field errors in span -->
              {{ fieldName }}:
              <template v-for="(item, index) in value">
                <span :key="index">{{item}}</span>
              </template>
            </template>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="dialogObject.dialog = false"
          >
            Dismiss
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
export default {
  name: 'FeedbackDialog',
  props: {
    dialogObject: {
      type: Object,
      required: true
    },
    riskModel: {
      type: Object,
      required: true
    }
  },
  computed: {
    riskFormLink () {
      return {
        name: 'risk-form',
        params: {
          id: this.dialogObject.data.id
        }
      }
    },
    riskModelLink () {
      return {
        name: 'risk-model-edit',
        params: {
          id: this.dialogObject.data.id
        }
      }
    }
  }
}
</script>
