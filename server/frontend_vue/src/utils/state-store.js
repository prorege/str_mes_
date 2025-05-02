export default new (class StateStore {
  constructor() {
    console.log('%cConstruct StateStore...', 'color:#337ab7');
    this.ver = '20220721-1';
    const storedVersion = localStorage.getItem('__mes_cache-version');
    if (!storedVersion || storedVersion !== this.ver) {
      localStorage.removeItem(this.STORAGE_KEY);
      localStorage.setItem('__mes_cache-version', this.ver);
    }

    this.STORAGE_KEY = 'state';

    try {
      let json = localStorage.getItem(this.STORAGE_KEY);
      if (!json) this.storage = {};
      else this.storage = JSON.parse(json);
    } catch (ex) {
      console.error(ex.message);
      this.storage = {};
    }

    const saveState = () => {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.storage));
    };
    window.removeEventListener('beforeunload', saveState);
    window.addEventListener('beforeunload', saveState);
  }

  clear () {
    localStorage.removeItem(this.STORAGE_KEY);
    this.storage = {}
  }

  bind(key, component) {
    // let loc = location.hash.replace(/\/\d+$/, '');
    let loc = location.pathname.replace(/\/\d+$/, '');
    loc = loc.split('?')[0];
    key = loc + '?' + key;
    switch (component.NAME) {
      case 'dxDataGrid':
        this.bindGrid(key, component);
        break;
      case 'dxPopup':
        this.bindPopup(key, component);
        break;
      case 'dxTreeList':
        this.bindTree(key, component);
        break;
      default:
        console.log(`No Control: ${component.NAME}`);
    }
  }

  bindPopup(key, popup) {
    console.log(`* bind popup %c${key}`, 'color:orange');
    const self = this;
    const savedOptions = self.storage[key];
    if (savedOptions) popup.option(savedOptions);
    else self.storage[key] = {};

    popup.option({
      onOptionChanged(evt) {
        if (['width', 'height'].includes(evt.name)) {
          self.storage[key][evt.name] = evt.value;
        }
      },
    });
  }

  bindGrid(key, grid) {
    console.log(`* bind grid %c${key}`, 'color:orange');
    const self = this;
    const savedOptions = self.storage[key];
    if (savedOptions && savedOptions.length) {
      for (let option of savedOptions) {
        grid.columnOption(option.name, option);
      }
    }

    if (!self.storage[key]) {
      self.storage[key] = grid.getController('columns')._columns.map((v) => ({
        name: v.name,
        width: v.visibleWidth,
        visible: v.visible,
        visibleIndex: v.visibleIndex,
      }));
    }

    grid.option({
      onOptionChanged(evt) {
        if (evt.name === 'columns') {
          // sortOrder가 빠지지 않아서 전체를 업데이트하도록 수정
          for (let i = 0; i < grid.columnCount(); i++) {
            const option = grid.columnOption(i);
            if (!option) continue;
            const index = option.index;
            self.storage[key][index] = {};
            self.storage[key][index]['name'] = option.name;
            self.storage[key][index]['visible'] = option.visible;
            self.storage[key][index]['visibleIndex'] = option.visibleIndex;
            self.storage[key][index]['width'] = option.width;
            self.storage[key][index]['sortOrder'] = option.sortOrder;
          }
          /*
          let matched = evt.fullName
            .match(/columns\[(\d+)\]\.([a-zA-Z]+)/)
            .splice(1, 2);
          let index = parseInt(matched[0], 10);
          let attributeName = matched[1];
          if (
            ['visible', 'visibleIndex', 'width', 'sortOrder'].includes(
              attributeName
            )
          ) {
            self.storage[key][index][attributeName] = evt.value;
          }
          */
        }
      },
    });
  }

  bindTree(key, tree) {
    console.log(`* bind tree %c${key}`, 'color:orange');
    const self = this;
    const savedOptions = self.storage[key];
    if (savedOptions && savedOptions.length) {
      for (let option of savedOptions) {
        tree.columnOption(option.name, option);
      }
    }

    if (!self.storage[key]) {
      self.storage[key] = tree.getController('columns')._columns.map((v) => ({
        name: v.name,
        width: v.visibleWidth,
        visible: v.visible,
        visibleIndex: v.visibleIndex,
      }));
    }

    tree.option({
      onOptionChanged(evt) {
        if (evt.name === 'columns') {
          // sortOrder가 빠지지 않아서 전체를 업데이트하도록 수정
          for (let i = 0; i < tree.columnCount(); i++) {
            const option = tree.columnOption(i);
            if (!option) continue;
            const index = option.index;
            self.storage[key][index] = {};
            self.storage[key][index]['name'] = option.name;
            self.storage[key][index]['visible'] = option.visible;
            self.storage[key][index]['visibleIndex'] = option.visibleIndex;
            self.storage[key][index]['width'] = option.width;
            self.storage[key][index]['sortOrder'] = option.sortOrder;
          }
        }
      },
    });
  }

})();
