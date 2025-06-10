import CustomStore from 'devextreme/data/custom_store';
import ApiService from '../utils/api-service';
import { exportDataGrid } from 'devextreme/excel_exporter';
import { Workbook } from 'exceljs';
import { saveAs } from 'file-saver';

export default class RestlessStore extends CustomStore {
  constructor(url, customOptions = {}, loadMode = 'processed', rowKey = 'id') {
    const apiService = new ApiService(url);
    const defaultFilters = [];

    let options = {
      // pk 컬럼 이름을 입력합니다
      key: rowKey,
      loadMode: loadMode,

      // GET ONE
      byKey(id) {
        if (typeof id === 'object') {
          const q = {filters: Object.keys(id).map(name => ({name, op: 'eq', val: id[name]}))}
          const params = {q: JSON.stringify(q)}

          return apiService.get('', {params}).then(response => {
            if (typeof this.transform === 'function') {
              try { this.transform(response.data) } catch(e) { console.debug(e) }
            }
            return response
          })
        }
        return apiService.get(`${id}`).then(response => {
          if (typeof this.transform === 'function') {
            try { this.transform(response.data) } catch(e) { console.debug(e) }
          }
          return response
        })
      },

      // GET MANY
      load(loadOptions) {
        let params = apiService.getParamsForRestless(
          loadOptions,
          this.defaultFilters
        );
        return apiService
          .get('', { params })
          .then((response) => {
            if (typeof this.transform === 'function') {
              try { this.transform(response.data.objects) } catch(e) { console.debug(e) }
            }
            return {
              data: response.data.objects,
              totalCount: response.data.num_results,
            };
          })
          .catch(() => {
            throw 'Network error';
          });
      },

      // POST ONE
      insert(values) {
        return apiService.post('', values);
      },

      // PATCH ONE
      update(id, values) {
        if (typeof id === 'object') {
          values.q = {filters: Object.keys(id).map(name => ({name, op: 'eq', val: id[name]}))}
          return apiService.patch('', values);
        }
        return apiService.patch(`${id}`, values);
      },

      // DELETE ONE
      remove(id) {
        return apiService.delete(`${id}`);
      },

      async exportData(component, sheetName, fileName) {
        const workbook = new Workbook();
        const worksheet = workbook.addWorksheet(sheetName);

        await exportDataGrid({ component, worksheet });
        const buffer = await workbook.xlsx.writeBuffer();
        saveAs(
          new Blob([buffer], { type: 'application/octet-stream' }),
          fileName
        );
      },
    };
    if (typeof customOptions === 'function') {
      const utils = { apiService };
      options = customOptions.call(utils, options, utils);
    } else if (typeof customOptions === 'object') {
      Object.assign(options, customOptions);
    }

    super(options);
    this._restlessApiConstructUrl = url;
    this._restlessApiConstructOptions = customOptions;
    this.defaultFilters = defaultFilters;
    this.getApiService = () => apiService;
    this.exportData = options.exportData;
    this.transform = null
  }

  clone(loadMode) {
    return new RestlessStore(
      this._restlessApiConstructUrl,
      this._restlessApiConstructOptions,
      loadMode
    );
  }
}
