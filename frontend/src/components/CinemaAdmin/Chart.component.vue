<script>
import { Bar } from 'vue-chartjs';

export default {
  name: 'Chart',
  extends: Bar,
  props: { data: { type: Object,
    default: function() {
      return { labels: 'None',
        datasets: [ { label: 'Number of visitors',
          backgroundColor: '#f87979',
          color: 'black',
          data: [] } ] };
    } } },
  mounted() {
    this.renderChart(
      this.data
    );
  }
};
</script>
