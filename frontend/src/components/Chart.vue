<script setup lang="ts">
import { fetchFundHistory } from '@/functions/db'
import { onMounted, useTemplateRef } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Legend,
  TimeScale,
  Title,
  Tooltip,
} from 'chart.js'
import 'chartjs-adapter-date-fns'

const ctx = useTemplateRef('ctx')

onMounted(async () => {
  const data = await fetchFundHistory([1], '2025-08-01', '2025-08-31')
  console.log(data[0])

  const offerData = data[0].prices.map((p) => ({ x: p.date, y: p.offer_price }))

  Chart.register(
    LineController,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Legend,
    TimeScale,
    Title,
    Tooltip,
  )

  Tooltip.positioners.myCustomPositioner = function (elements, eventPosition) {
    const tooltip = this
    const chart = this.chart
    const chartArea = chart.chartArea
    let x = eventPosition.x
    let y = eventPosition.y

    // Default offset distance from cursor
    const offset = 10

    // If cursor is in the left half of chart, show tooltip to the right
    if (eventPosition.x < (chartArea.left + chartArea.right) / 2) {
      x = eventPosition.x + offset
    } else {
      // If in right half, show to the left
      x = eventPosition.x - offset
    }

    return { x, y }
  }

  new Chart(ctx.value, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'title',
          data: offerData,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'hi' + ' (Aug 2025)',
        },
        tooltip: {
          animation: false,
          mode: 'index',
          intersect: false,
          position: 'nearest',
          callbacks: {
            label: function (context) {
              const value = context.raw.y.toFixed(3) // show 3 decimals
              return value
            },
            title: function (context) {
              return context[0].raw.x
            },
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'day',
            tooltipFormat: 'MMM dd', // hover shows full date
            displayFormats: {
              day: 'dd', // show only day on x-axis
            },
          },
          ticks: {
            autoSkip: true,
            maxRotation: 0,
            minRotation: 0,
            autoSkipPadding: 20,
            callback: function (value, index, ticks) {
              // Show regular date labels for most ticks
              const date = new Date(value)

              // For the last tick, show just the month
              if (index === ticks.length - 1) {
                return date.toLocaleDateString('en-US', { month: 'short' })
              }

              // For other ticks, show month and day
              return date.toLocaleDateString('en-US', {
                day: 'numeric',
              })
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'Bid Price',
          },
          beginAtZero: false,
        },
      },
    },
  })
})
</script>

<template>
  <canvas ref="ctx"></canvas>
</template>
