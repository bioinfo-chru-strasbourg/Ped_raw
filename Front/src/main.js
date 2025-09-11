import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import PrimeVue from 'primevue/config';
import 'primeicons/primeicons.css';
import "primevue/resources/themes/lara-light-blue/theme.css";
import "primevue/resources/primevue.min.css";
import JsonCSV from 'vue-json-csv'





import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Toolbar from 'primevue/toolbar';
import InputText from 'primevue/inputtext';
import Tag from 'primevue/tag';
import FileUpload from 'primevue/fileupload';
import Column from 'primevue/column';
import BadgeDirective from "primevue/badgedirective";
import BlockUI from 'primevue/blockui';
import Card from 'primevue/card';
import Checkbox from 'primevue/checkbox';
import Chip from 'primevue/chip';
import Chips from 'primevue/chips';
import ConfirmDialog from 'primevue/confirmdialog';
import DataView from 'primevue/dataview';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import FocusTrap from 'primevue/focustrap';
import InlineMessage from 'primevue/inlinemessage';
import Message from 'primevue/message';
import MultiSelect from 'primevue/multiselect';
import Paginator from 'primevue/paginator';
import Panel from 'primevue/panel';
import PanelMenu from 'primevue/panelmenu';
import Ripple from 'primevue/ripple';
import Row from 'primevue/row';
import SelectButton from 'primevue/selectbutton';
import Skeleton from 'primevue/skeleton';
import StyleClass from 'primevue/styleclass';
import TabMenu from 'primevue/tabmenu';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import ToggleButton from 'primevue/togglebutton';
import Tooltip from 'primevue/tooltip';



const app = createApp(App)
app.use(router)
app.component('downloadCsv', JsonCSV);

app.use(PrimeVue, { ripple: true });
app.component('Button', Button);
app.component('DataTable', DataTable);
app.component('Toolbar', Toolbar);
app.component('InputText', InputText);
app.component('Tag', Tag);
app.component('FileUpload', FileUpload);
app.component('Column', Column);
app.directive('tooltip', Tooltip);
app.directive('badge', BadgeDirective);
app.directive('ripple', Ripple);
app.directive('styleclass', StyleClass);
app.directive('focustrap', FocusTrap);
app.component('BlockUI', BlockUI);
app.component('Card', Card);
app.component('Checkbox', Checkbox);
app.component('Chip', Chip);
app.component('Chips', Chips);
app.component('ConfirmDialog', ConfirmDialog);
app.component('DataView', DataView);
app.component('Dialog', Dialog);
app.component('Dropdown', Dropdown);
app.component('InlineMessage', InlineMessage);
app.component('Message', Message);
app.component('MultiSelect', MultiSelect);
app.component('Paginator', Paginator);
app.component('Panel', Panel);
app.component('PanelMenu', PanelMenu);
app.component('Row', Row);
app.component('SelectButton', SelectButton);
app.component('Skeleton', Skeleton);
app.component('TabMenu', TabMenu);
app.component('TabView', TabView);
app.component('TabPanel', TabPanel);
app.component('ToggleButton', ToggleButton)





app.mount('#app')