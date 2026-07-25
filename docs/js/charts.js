// ============================================================
// PROJETO MARINGÁ — RENDERIZAÇÃO DE GRÁFICOS INTERATIVOS (CHART.JS)
// COM PALETA EM TONS TERROSOS E DESIGN LIMPO
// ============================================================

let orgsChart = null;
let comdemaChart = null;

window.renderCharts = function(orgsByGroup) {
    const ctxOrgs = document.getElementById('chart-orgs-group');
    if (!ctxOrgs) return;

    if (orgsChart) orgsChart.destroy();

    const labels = Object.keys(orgsByGroup || {});
    const dataValues = Object.values(orgsByGroup || {});

    // Paleta de tons terrosos e naturais
    const colors = ['#4A3B32', '#B86B43', '#5E7A68', '#D9A27F'];

    orgsChart = new Chart(ctxOrgs, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#FFFFFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { family: 'Plus Jakarta Sans', size: 12 },
                        color: '#2C221E',
                        padding: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const val = context.raw;
                            const pct = ((val / total) * 100).toFixed(1);
                            return ` ${context.label}: ${val} orgs (${pct}%)`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
};

window.renderComdemaTimeline = function(yearlyStats) {
    const ctxComdema = document.getElementById('chart-comdema-timeline');
    if (!ctxComdema) return;

    if (comdemaChart) comdemaChart.destroy();

    const years = yearlyStats.map(s => s.year);
    const publicCounts = yearlyStats.map(s => s.public_count);
    const privateCounts = yearlyStats.map(s => s.private_count);
    const academiaCounts = yearlyStats.map(s => s.academia_count);
    const civilCounts = yearlyStats.map(s => s.soc_civil_count);

    comdemaChart = new Chart(ctxComdema, {
        type: 'bar',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Público',
                    data: publicCounts,
                    backgroundColor: '#4A3B32',
                    borderRadius: 2
                },
                {
                    label: 'Privado',
                    data: privateCounts,
                    backgroundColor: '#B86B43',
                    borderRadius: 2
                },
                {
                    label: 'Academia',
                    data: academiaCounts,
                    backgroundColor: '#D9A27F',
                    borderRadius: 2
                },
                {
                    label: 'Sociedade Civil',
                    data: civilCounts,
                    backgroundColor: '#5E7A68',
                    borderRadius: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true,
                    grid: { display: false },
                    ticks: { color: '#2C221E', font: { family: 'Plus Jakarta Sans', size: 12 } }
                },
                y: {
                    stacked: true,
                    grid: { color: '#E2D7CC' },
                    ticks: { color: '#2C221E', font: { family: 'Plus Jakarta Sans', size: 12 } }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { font: { family: 'Plus Jakarta Sans', size: 12 }, color: '#2C221E' }
                }
            }
        }
    });
};
