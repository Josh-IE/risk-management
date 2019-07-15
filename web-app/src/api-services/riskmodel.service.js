import Axios from 'axios'

const RESOURCE_NAME = '/risk_model'

export default {
  /**
   * getAll() returns an axios request promise object that retrieves a list of all risk models.
   * @return {Promise} GET request Promise object.
   */
  getAll () {
    return Axios.get(RESOURCE_NAME)
  },

  /**
   * get() returns an axios request promise object that retrieves a risk model.
   * @param {number} id  risk model id.
   * @return {Promise} GET request Promise object.
   */
  get (id) {
    return Axios.get(`${RESOURCE_NAME}/${id}/`)
  },

  /**
   * create() returns an axios request promise object that creates a risk model.
   * @param {object} data  risk model data.
   * @return {Promise} POST request Promise object.
   */
  create (data) {
    return Axios.post(`${RESOURCE_NAME}/`, data)
  },

  /**
   * update() returns an axios request promise object that updates an existing risk model.
   * @param {id} data  risk model id.
   * @param {object} data  risk model data.
   * @return {Promise} PUT request Promise object.
   */
  update (id, data) {
    return Axios.put(`${RESOURCE_NAME}/${id}/`, data)
  },

  /**
   * getFieldTypes() returns an axios request promise object that retrieves the list of field types.
   * @return {Promise} GET request Promise object.
   */
  getFieldTypes () {
    return Axios.get(`${RESOURCE_NAME}/field_types/`)
  }

  // FIXME: implement risk model delete
  /**
   *delete (id) {
   *return Axios.delete(`${RESOURCE_NAME}/${id}`)
  }
  */
}
