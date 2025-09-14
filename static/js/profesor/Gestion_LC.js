document.addEventListener('DOMContentLoaded', () => {

    // --- MÓDULO DE UTILIDADES (MODALES Y VISTAS) ---
    const UI = (() => {
        const attendanceTab = document.getElementById('attendance-tab');
        const gradesTab = document.getElementById('grades-tab');
        const attendanceContent = document.getElementById('attendance-content');
        const gradesContent = document.getElementById('grades-content');

        const alertModal = document.getElementById('alertModal');
        const alertModalBody = document.getElementById('alertModalBody');
        const promptModal = document.getElementById('promptModal');
        const confirmModal = document.getElementById('confirmModal');

        const switchView = (activeTab, activeContent, inactiveTab, inactiveContent) => {
            activeTab.classList.add('active');
            inactiveTab.classList.remove('active');
            activeContent.style.display = 'block';
            inactiveContent.style.display = 'none';
        };

        const showModal = (modal, setup) => {
            setup();
            modal.classList.add('show');
        };

        const hideModal = (modal) => modal.classList.remove('show');

        const showAlert = (message) => {
            showModal(alertModal, () => {
                alertModalBody.innerHTML = message.replace(/\n/g, '<br>');
                document.getElementById('alertModalAcceptBtn').onclick = () => hideModal(alertModal);
            });
        };

        const showPrompt = (title, body, callback) => {
            showModal(promptModal, () => {
                promptModal.querySelector('#promptModalTitle').textContent = title;
                promptModal.querySelector('#promptModalBody').textContent = body;
                const input = promptModal.querySelector('#promptModalInput');
                input.value = '';

                const confirmBtn = promptModal.querySelector('#promptModalConfirmBtn');
                const cancelBtn = promptModal.querySelector('#promptModalCancelBtn');
                confirmBtn.onclick = () => { hideModal(promptModal); callback(input.value); };
                cancelBtn.onclick = () => { hideModal(promptModal); callback(null); };
            });
        };

        const showConfirm = (body, callback) => {
            showModal(confirmModal, () => {
                confirmModal.querySelector('#confirmModalBody').textContent = body;
                const confirmBtn = confirmModal.querySelector('#confirmModalConfirmBtn');
                const cancelBtn = confirmModal.querySelector('#confirmModalCancelBtn');
                confirmBtn.onclick = () => { hideModal(confirmModal); callback(true); };
                cancelBtn.onclick = () => { hideModal(confirmModal); callback(false); };
            });
        };

        return { switchView, showAlert, showPrompt, showConfirm, attendanceTab, gradesTab, attendanceContent, gradesContent };
    })();

    // --- DATOS GLOBALES ---
    let students = [
        { id: 'AS', name: 'Alice Smith', grades: [] },
        { id: 'BJ', name: 'Bob Johnson', grades: [] },
        { id: 'CB', name: 'Charlie Brown', grades: [] },
        { id: 'DP', name: 'Diana Prince', grades: [] },
        { id: 'EH', name: 'Ethan Hunt', grades: [] },
    ];
    let assignmentNames = [];
    let attendanceData = {};
    
    // --- MÓDULO DE ASISTENCIA ---
    const AttendanceModule = (() => {
        const monthlyView = document.getElementById('monthly-view');
        const dailyView = document.getElementById('daily-view');
        const monthYearDisplay = document.getElementById('month-year-display');
        const monthlyTableHead = document.querySelector('.monthly-grid-table thead');
        const monthlyTableBody = document.querySelector('.monthly-grid-table tbody');
        const dailyViewTitle = document.getElementById('daily-view-title');

        let currentDisplayDate = new Date();
        let selectedDateForDailyView = null;

        const countUnexcusedAbsences = (studentId, year, month) => {
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            let unexcusedCount = 0;
            for (let i = 1; i <= daysInMonth; i++) {
                const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                const studentData = attendanceData[dateKey]?.[studentId];
                if (studentData?.absent && !studentData.excuse) {
                    unexcusedCount++;
                }
            }
            return unexcusedCount;
        };

        const renderMonthlyList = (year, month) => {
            monthYearDisplay.textContent = new Date(year, month).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
            monthlyTableHead.innerHTML = `<tr><th class="student-name-header">Estudiante</th>${Array.from({ length: new Date(year, month + 1, 0).getDate() }, (_, i) => {
                const day = i + 1;
                const date = new Date(year, month, day);
                const isToday = date.setHours(0, 0, 0, 0) === new Date().setHours(0, 0, 0, 0);
                return `<th class="day-header ${isToday ? 'today' : ''}" data-day="${day}">${day}</th>`;
            }).join('')}</tr>`;

            monthlyTableBody.innerHTML = students.map(student => {
                const unexcusedAbsences = countUnexcusedAbsences(student.id, year, month);
                const rowClass = unexcusedAbsences >= 3 ? 'highlight-absentee' : '';
                const days = Array.from({ length: new Date(year, month + 1, 0).getDate() }, (_, i) => {
                    const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`;
                    const studentData = attendanceData[dateKey]?.[student.id];
                    const status = studentData ? (studentData.absent ? 'absent' : (studentData.late ? 'late' : (studentData.present ? 'present' : null))) : '';
                    const hasExcuse = studentData?.excuse ? '<div class="excuse-dot"></div>' : '';
                    return `<td><div class="status-indicator ${status}">${hasExcuse}</div></td>`;
                }).join('');
                return `<tr class="${rowClass}"><td class="student-name-cell">${student.name}</td>${days}</tr>`;
            }).join('');
        };

        const showDailyView = (date) => {
            selectedDateForDailyView = date;
            dailyViewTitle.textContent = `Asistencia para ${date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })}`;
            populateStudentListForDay(date);
            monthlyView.style.display = 'none';
            dailyView.style.display = 'block';
        };

        const populateStudentListForDay = (date) => {
            const studentListContainer = dailyView.querySelector('.student-list');
            const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
            studentListContainer.innerHTML = `<div class="list-header"><span class="student-name-header-daily">Nombre del Estudiante</span><span class="attendance-status-header">Estado de Asistencia</span></div>${students.map(student => {
                const studentData = attendanceData[dateKey]?.[student.id];
                const isAbsent = studentData?.absent || false;
                const isLate = studentData?.late || false;
                const isPresent = studentData?.present || false;
                const hasExcuse = studentData?.excuse || false;
                return `<div class="student-row" data-student-id="${student.id}"><div class="student-info"><div class="avatar-small">${student.id}</div><span>${student.name}</span></div><div class="attendance-controls"><button class="status-btn present ${isPresent ? 'selected' : ''}">Presente</button><button class="status-btn absent ${isAbsent ? 'selected' : ''}">Ausente</button><button class="status-btn late ${isLate ? 'selected' : ''}">Tarde</button><div class="excuse-container" style="display: ${isAbsent || isLate ? 'flex' : 'none'};"><label class="excuse-label"><input type="checkbox" class="excuse-checkbox" ${hasExcuse ? 'checked' : ''}> Trajo Excusa</label></div></div></div>`;
            }).join('')}`;
            setupDailyViewLogic();
        };

        const setupDailyViewLogic = () => {
            const studentRows = dailyView.querySelectorAll('.student-row');
            const presentCountEl = document.getElementById('present-count');
            const absentCountEl = document.getElementById('absent-count');
            const lateCountEl = document.getElementById('late-count');
            
            const updateSummary = () => {
                let present = 0, absent = 0, late = 0;
                studentRows.forEach(row => {
                    if (row.querySelector('.status-btn.present').classList.contains('selected')) present++;
                    if (row.querySelector('.status-btn.absent').classList.contains('selected')) absent++;
                    if (row.querySelector('.status-btn.late').classList.contains('selected')) late++;
                });
                presentCountEl.textContent = present;
                absentCountEl.textContent = absent;
                lateCountEl.textContent = late;
            };

            const updateExcuseVisibility = (row) => {
                const isAbsentOrLate = row.querySelector('.status-btn.absent').classList.contains('selected') || row.querySelector('.status-btn.late').classList.contains('selected');
                row.querySelector('.excuse-container').style.display = isAbsentOrLate ? 'flex' : 'none';
                if (!isAbsentOrLate) row.querySelector('.excuse-checkbox').checked = false;
            };

            studentRows.forEach(row => {
                const btns = row.querySelectorAll('.status-btn');
                btns.forEach(btn => {
                    btn.addEventListener('click', () => {
                        const status = btn.classList[1]; // present, absent, late
                        const presentBtn = row.querySelector('.status-btn.present');
                        const absentBtn = row.querySelector('.status-btn.absent');
                        const lateBtn = row.querySelector('.status-btn.late');

                        if (status === 'present') {
                            presentBtn.classList.toggle('selected');
                            absentBtn.classList.remove('selected');
                            if (!presentBtn.classList.contains('selected')) lateBtn.classList.remove('selected');
                        } else if (status === 'absent') {
                            absentBtn.classList.toggle('selected');
                            if (absentBtn.classList.contains('selected')) {
                                presentBtn.classList.remove('selected');
                                lateBtn.classList.remove('selected');
                            }
                        } else if (status === 'late') {
                            lateBtn.classList.toggle('selected');
                            if (lateBtn.classList.contains('selected')) {
                                presentBtn.classList.add('selected');
                                absentBtn.classList.remove('selected');
                            }
                        }
                        updateExcuseVisibility(row);
                        updateSummary();
                    });
                });
            });
            updateSummary();
        };

        const saveDailyAttendance = () => {
            const date = selectedDateForDailyView;
            const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
            attendanceData[dateKey] = {};
            dailyView.querySelectorAll('.student-row').forEach(row => {
                const studentId = row.dataset.studentId;
                const isPresent = row.querySelector('.status-btn.present').classList.contains('selected');
                const isAbsent = row.querySelector('.status-btn.absent').classList.contains('selected');
                const isLate = row.querySelector('.status-btn.late').classList.contains('selected');
                const hasExcuse = row.querySelector('.excuse-checkbox').checked;
                if (isPresent || isAbsent || isLate) {
                    attendanceData[dateKey][studentId] = { present: isPresent, absent: isAbsent, late: isLate, excuse: hasExcuse };
                }
            });
            UI.showAlert('Asistencia guardada!');
            showMonthlyView();
        };

        const setupEventListeners = () => {
            document.getElementById('prev-month-btn').addEventListener('click', () => {
                currentDisplayDate.setMonth(currentDisplayDate.getMonth() - 1);
                renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth());
            });
            document.getElementById('next-month-btn').addEventListener('click', () => {
                currentDisplayDate.setMonth(currentDisplayDate.getMonth() + 1);
                renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth());
            });
            document.getElementById('go-to-today-btn').addEventListener('click', () => showDailyView(new Date()));
            document.getElementById('back-to-monthly-btn').addEventListener('click', () => showMonthlyView());
            document.getElementById('save-daily-attendance-btn').addEventListener('click', saveDailyAttendance);
            monthlyTableHead.addEventListener('click', (e) => {
                if (e.target.dataset.day) {
                    const day = parseInt(e.target.dataset.day);
                    showDailyView(new Date(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth(), day));
                }
            });
        };

        return { init: () => { setupEventListeners(); renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth()); } };
    })();

    // --- MÓDULO DE CALIFICACIONES ---
    const GradesModule = (() => {
        const gradesTable = document.querySelector('.grades-table');
        const gradesTableHead = gradesTable.querySelector('thead');
        const gradesTableBody = gradesTable.querySelector('tbody');
        const lowestGradeEl = document.getElementById('lowest-grade');
        const highestGradeEl = document.getElementById('highest-grade');
        const averageGradeEl = document.getElementById('average-grade');
        const passingGradeInput = document.getElementById('passing-grade');
        const minGradeInput = document.getElementById('min-grade');
        const maxGradeInput = document.getElementById('max-grade');

        const calculateAllAverages = () => {
            let allGrades = [];
            const passingGrade = parseFloat(passingGradeInput.value) || 60;

            gradesTableBody.querySelectorAll('tr').forEach((row, studentIndex) => {
                let sum = 0, count = 0;
                row.querySelectorAll('.grade-input').forEach((input, gradeIndex) => {
                    const value = parseFloat(input.value);
                    if (!isNaN(value)) {
                        sum += value;
                        count++;
                        allGrades.push(value);
                    }
                    students[studentIndex].grades[gradeIndex] = isNaN(value) ? '' : value;
                });
                const average = count > 0 ? (sum / count).toFixed(1) : 'N/A';
                const averageCell = row.querySelector('.average-cell');
                averageCell.textContent = average;
                averageCell.classList.toggle('failing', average !== 'N/A' && parseFloat(average) < passingGrade);
                row.classList.toggle('failing-student', average !== 'N/A' && parseFloat(average) < passingGrade);
            });

            if (allGrades.length > 0) {
                lowestGradeEl.textContent = Math.min(...allGrades).toFixed(1);
                highestGradeEl.textContent = Math.max(...allGrades).toFixed(1);
                averageGradeEl.textContent = (allGrades.reduce((a, b) => a + b, 0) / allGrades.length).toFixed(1);
            } else {
                lowestGradeEl.textContent = '0';
                highestGradeEl.textContent = '0';
                averageGradeEl.textContent = '0';
            }
        };

        const renderGradesTable = () => {
            gradesTableHead.innerHTML = `<tr><th class="student-name-header">Nombre</th>${assignmentNames.map(name =>
                `<th><span>${name}</span> <span class="assignment-actions"><i class="fas fa-pencil-alt" data-action="edit-assignment"></i><i class="fas fa-trash-alt delete-assignment-icon" data-action="delete-assignment"></i></span></th>`
            ).join('')}<th>Promedio</th></tr>`;

            gradesTableBody.innerHTML = students.map(student =>
                `<tr data-student-id="${student.id}"><td class="student-name-cell">${student.name}</td>${student.grades.map(grade =>
                    `<td><input type="number" class="grade-input" value="${grade}"></td>`
                ).join('')}<td class="average-cell">0</td></tr>`
            ).join('');
            
            calculateAllAverages();
        };

        const setupEventListeners = () => {
            document.getElementById('add-assignment-btn').addEventListener('click', () => {
                UI.showPrompt("Nueva Asignación", "Introduce el nombre de la nueva asignación:", (name) => {
                    if (name && name.trim() !== '') {
                        assignmentNames.push(name.trim());
                        students.forEach(student => student.grades.push(''));
                        renderGradesTable();
                    }
                });
            });

            gradesTableHead.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (!action) return;
                const headerCell = e.target.closest('th');
                const columnIndex = Array.from(headerCell.parentNode.children).indexOf(headerCell) - 1;
                const currentName = assignmentNames[columnIndex];

                if (action === 'delete-assignment') {
                    UI.showConfirm(`¿Estás seguro de que quieres eliminar la columna "${currentName}"?`, (confirmed) => {
                        if (confirmed) {
                            assignmentNames.splice(columnIndex, 1);
                            students.forEach(student => student.grades.splice(columnIndex, 1));
                            renderGradesTable();
                        }
                    });
                } else if (action === 'edit-assignment') {
                    UI.showPrompt('Editar Asignación', `Introduce el nuevo nombre para "${currentName}":`, (newName) => {
                        if (newName && newName.trim() !== '') {
                            assignmentNames[columnIndex] = newName.trim();
                            renderGradesTable();
                        }
                    });
                }
            });

            gradesTableBody.addEventListener('change', (e) => {
                if (e.target.classList.contains('grade-input')) {
                    const value = parseFloat(e.target.value);
                    const min = parseFloat(minGradeInput.value);
                    const max = parseFloat(maxGradeInput.value);
                    if (e.target.value !== '' && (value < min || value > max)) {
                        e.target.value = '';
                    }
                    calculateAllAverages();
                }
            });

            document.querySelectorAll('.grades-settings input').forEach(input => {
                input.addEventListener('change', calculateAllAverages);
            });
        };

        return { init: () => { setupEventListeners(); renderGradesTable(); } };
    })();

    // --- INICIALIZACIÓN GENERAL ---
    UI.attendanceTab.addEventListener('click', () => UI.switchView(UI.attendanceTab, UI.attendanceContent, UI.gradesTab, UI.gradesContent));
    UI.gradesTab.addEventListener('click', () => UI.switchView(UI.gradesTab, UI.gradesContent, UI.attendanceTab, UI.attendanceContent));

    AttendanceModule.init();
    GradesModule.init();
});