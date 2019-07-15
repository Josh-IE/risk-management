export default {
  /**
   * nullBlankFields() replaces the blank values in a risk model object with null.
   * @param {object} riskmodel  riskmodel json object.
   * @return {object} riskmodel json object.
   */
  nullBlankFields (data) {
    let self = this
    for (const key of Object.keys(data)) {
      if (data[key] === '') {
        data[key] = null
      } else if (key === 'fields') {
        data.fields.forEach(function (field, index) {
          self.nullBlankFields(field)
        })
      }
    }
    return data
  },

  /**
   * move() reorders the position of elements in an array.
   * @param {object} array  array of objects.
   * @param {object} element element to be repositioned.
   * @param {number} delta margin between old and new position.
   * @return {null} N/A.
   */
  move (array, element, delta) {
    var index = array.indexOf(element)
    var newIndex = index + delta

    // Already at the top or bottom.
    if (newIndex < 0 || newIndex === array.length) return

    var indexes = [index, newIndex].sort((a, b) => a - b)

    // Replace from lowest index, two elements, reverting the order
    array.splice(indexes[0], 2, array[indexes[1]], array[indexes[0]])
  },

  /**
   * refreshFieldOrder() updates the 'order' key of all the objects in an array to the 1-based index of the object.
   * @param {object} array  list of objects.
   * @return {null} N/A.
   */
  refreshFieldOrder (array) {
    array.forEach(function (field, index) {
      field.order = index + 1
    })
  }
}
