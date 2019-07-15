// Field component: Renders the Fields of a RiskModel
<template>
  <v-layout
    row
    xs12
    md12
  >
    <v-flex xs12>
      <v-card
        xs12
        md12
      >
        <v-container>
          <v-toolbar
            card
            color="blue"
            dark
          >
            <v-toolbar-title>
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn
                    depressed
                    small
                    @="on"
                  >{{field.order}}
                  </v-btn>
                </template>
                <span>Field Position</span>
              </v-tooltip>
              {{field.name}}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template #activator="{ on }">
                <v-icon
                  @click="$emit('moveUp')"
                  @="on"
                >arrow_upward</v-icon>
              </template>
              <span>Move Field Position Up</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on }">
                <v-icon
                  @click="$emit('moveDown')"
                  @="on"
                  class="ml-4"
                >arrow_downward</v-icon>
              </template>
              <span>Move Field Position Down</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on }">
                <v-icon
                  @click="$emit('remove')"
                  @="on"
                  class="ml-4"
                >close</v-icon>
              </template>
              <span>Remove Field</span>
            </v-tooltip>
          </v-toolbar>
          <v-layout
            row
            wrap
          >
            <v-flex
              xs12
              md6
            >
              <v-text-field
                v-model="field.name"
                :counter="255"
                label="Label*"
                hint="Field Name"
                required
                outline
              ></v-text-field>
            </v-flex>
            <v-flex md6>
              <v-autocomplete
                v-model="field.field_type"
                :items="fieldTypeChoices"
                label="Field Type*"
                persistent-hint
                hint="Field Type. Submitted data would be validated against this Field type."
                required
                outline
              ></v-autocomplete>
            </v-flex>
            <template v-if="['email', 'password', 'regex', 'text', 'textarea', 'url'].includes(field.field_type)">
              <v-flex md6>
                <v-text-field
                  v-model="field.min_length"
                  :counter="255"
                  hint="Value must be <= FIELD_MAX_LENGTH"
                  label="Min. Length"
                  required
                  outline
                ></v-text-field>
              </v-flex>
              <v-flex md6>
                <v-text-field
                  v-model="field.max_length"
                  :counter="255"
                  hint="Value must be <= FIELD_MAX_LENGTH"
                  label="Max. Length"
                  type="number"
                  required
                  outline
                ></v-text-field>
              </v-flex>
            </template>
            <v-flex
              xs12
              md6
              v-if="field.field_type === 'regex'"
            >
              <v-text-field
                v-model="field.regex_pattern"
                :counter="255"
                label="Regex Pattern*"
                hint="Search is made against this pattern."
                required
                outline
              ></v-text-field>
            </v-flex>
            <v-flex
              md6
              v-if="['select', 'multiselect', 'radio'].includes(field.field_type)"
            >
              <v-combobox
                v-model="field.choices"
                :items=[]
                label="Choices"
                hint="Provide the choices, use the return key to Enter"
                multiple
                outline
                chips
              ></v-combobox>
            </v-flex>
            <v-flex
              xs12
              md6
              v-if="!['array', 'checkbox', 'file', 'multiselect', 'switch'].includes(field.field_type)"
            >
              <v-text-field
                v-model="field.default"
                :counter="255"
                label="Default value"
                hint="Field's default value "
                required
                outline
              ></v-text-field>
            </v-flex>
            <v-flex
              xs12
              md6
            >
              <v-text-field
                v-model="field.help_text"
                :counter="255"
                label="Help Text"
                hint="Textual aid about the field"
                required
                outline
              ></v-text-field>
            </v-flex>
            <v-flex md6>
              <v-checkbox
                v-if="!['checkbox', 'switch'].includes(field.field_type)"
                v-model="field.required"
                label="Required?"
                persistent-hint
                hint="Required fields are made compulsory"
                required
              ></v-checkbox>
            </v-flex>
            <v-flex md6>
              <v-checkbox
                v-if="field.field_type!='file'"
                v-model="field.unique"
                label="Unique?"
                persistent-hint
                hint="Unique fields wont accept duplicate entries"
                required
              ></v-checkbox>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'Field',
  props: {
    field: {
      type: Object,
      required: true
    },
    fieldTypeChoices: {
      type: Array,
      required: true
    }
  },
  watch: {
    'field.field_type' (val, oldval) {
      this.field.default = null
      this.field.choices = null
    }
  }
}
</script>
