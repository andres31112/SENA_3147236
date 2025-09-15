
document.addEventListener('DOMContentLoaded', () => {
    // --- GENERAL & VIEW SWITCHING ---
    const attendanceTab = document.getElementById('attendance-tab');
    const gradesTab = document.getElementById('grades-tab');
    const attendanceContent = document.getElementById('attendance-content');
    const gradesContent = document.getElementById('grades-content');

    attendanceTab.addEventListener('click', () => {
        attendanceTab.classList.add('active');
        gradesTab.classList.remove('active');
        attendanceContent.style.display = 'block';
        gradesContent.style.display = 'none';
    });
    gradesTab.addEventListener('click', () => {
        gradesTab.classList.add('active');
        attendanceTab.classList.remove('active');
        gradesContent.style.display = 'block';
        attendanceContent.style.display = 'none';
    });

    // --- DATA ---
    let students = [
        { id: 'AS', name: 'Alice Smith', grades: [] },
        { id: 'BJ', name: 'Bob Johnson', grades: [] },
        { id: 'CB', name: 'Charlie Brown', grades: [] },
        { id: 'DP', name: 'Diana Prince', grades: [] },
        { id: 'EH', name: 'Ethan Hunt', grades: [] },
    ];
    let assignmentNames = [];
    let attendanceData = {}; 

    // --- MODAL LOGIC ---
    const alertModal = document.getElementById('alertModal');
    const alertModalBody = document.getElementById('alertModalBody');
    const alertModalAcceptBtn = document.getElementById('alertModalAcceptBtn');
    const showAlert = (message) => {
        alertModalBody.innerHTML = message.replace(/\n/g, '<br>'); // Support line breaks
        alertModal.classList.add('show');
    };
    alertModalAcceptBtn.addEventListener('click', () => alertModal.classList.remove('show'));

    const promptModal = document.getElementById('promptModal');
    const showPrompt = (title, body, callback) => {
        promptModal.querySelector('#promptModalTitle').textContent = title;
        promptModal.querySelector('#promptModalBody').textContent = body;
        const input = promptModal.querySelector('#promptModalInput');
        input.value = '';
        promptModal.classList.add('show');
        
        const confirmBtn = promptModal.querySelector('#promptModalConfirmBtn');
        const cancelBtn = promptModal.querySelector('#promptModalCancelBtn');

        const confirmHandler = () => {
            promptModal.classList.remove('show');
            callback(input.value);
            cleanup();
        };
        const cancelHandler = () => {
            promptModal.classList.remove('show');
            callback(null);
            cleanup();
        };
        const cleanup = () => {
            confirmBtn.removeEventListener('click', confirmHandler);
            cancelBtn.removeEventListener('click', cancelHandler);
        };

        confirmBtn.addEventListener('click', confirmHandler);
        cancelBtn.addEventListener('click', cancelHandler);
    };

    const confirmModal = document.getElementById('confirmModal');
    const showConfirm = (body, callback) => {
        confirmModal.querySelector('#confirmModalBody').textContent = body;
        confirmModal.classList.add('show');
        const confirmBtn = confirmModal.querySelector('#confirmModalConfirmBtn');
        const cancelBtn = confirmModal.querySelector('#confirmModalCancelBtn');

        const confirmHandler = () => {
            confirmModal.classList.remove('show');
            callback(true);
            cleanup();
        };
        const cancelHandler = () => {
            confirmModal.classList.remove('show');
            callback(false);
            cleanup();
        };
            const cleanup = () => {
            confirmBtn.removeEventListener('click', confirmHandler);
            cancelBtn.removeEventListener('click', cancelHandler);
        };

        confirmBtn.addEventListener('click', confirmHandler);
        cancelBtn.addEventListener('click', cancelHandler);
    };


    // --- ATTENDANCE LOGIC ---
    const monthlyView = document.getElementById('monthly-view');
    const dailyView = document.getElementById('daily-view');
    const monthYearDisplay = document.getElementById('month-year-display');
    const monthlyTableHead = document.querySelector('.monthly-grid-table thead');
    const monthlyTableBody = document.querySelector('.monthly-grid-table tbody');
    const prevMonthBtn = document.getElementById('prev-month-btn');
    const nextMonthBtn = document.getElementById('next-month-btn');
    const goToTodayBtn = document.getElementById('go-to-today-btn');
    const backToMonthlyBtn = document.getElementById('back-to-monthly-btn');
    const dailyViewTitle = document.getElementById('daily-view-title');
    let currentDisplayDate = new Date();
    let selectedDateForDailyView = null;

    const showMonthlyView = () => {
        renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth());
        monthlyView.style.display = 'block';
        dailyView.style.display = 'none';
    };
    const showDailyView = (date) => {
        selectedDateForDailyView = date;
        dailyViewTitle.textContent = `Asistencia para ${date.toLocaleDateString('es-ES', {weekday: 'long', day: 'numeric', month: 'long'})}`;
        populateStudentListForDay(date);
        monthlyView.style.display = 'none';
        dailyView.style.display = 'block';
    };
    const countUnexcusedAbsences = (studentId, year, month) => {
        let unexcusedCount = 0;
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        for (let i = 1; i <= daysInMonth; i++) {
            const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const studentData = attendanceData[dateKey]?.[studentId];
            if (studentData && studentData.absent && !studentData.excuse) {
                unexcusedCount++;
            }
        }
        return unexcusedCount;
    };
    const renderMonthlyList = (year, month) => {
        monthYearDisplay.textContent = new Date(year, month).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
        monthlyTableHead.innerHTML = '';
        monthlyTableBody.innerHTML = '';
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `<th class="student-name-header">Estudiante</th>`;
        for (let i = 1; i <= daysInMonth; i++) {
            const th = document.createElement('th');
            th.classList.add('day-header');
            th.textContent = i;
            const thisDate = new Date(year, month, i);
            if (thisDate.setHours(0,0,0,0) === today.setHours(0,0,0,0)) {
                th.classList.add('today');
            }
            th.addEventListener('click', () => showDailyView(thisDate));
            headerRow.appendChild(th);
        }
        monthlyTableHead.appendChild(headerRow);
        students.forEach(student => {
            const studentRow = document.createElement('tr');
            const unexcusedAbsences = countUnexcusedAbsences(student.id, year, month);
            if (unexcusedAbsences >= 3) {
                studentRow.classList.add('highlight-absentee');
            }
            studentRow.innerHTML = `<td class="student-name-cell">${student.name}</td>`;
            for (let i = 1; i <= daysInMonth; i++) {
                const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                const studentData = attendanceData[dateKey]?.[student.id];
                const status = studentData ? (studentData.absent ? 'absent' : (studentData.late ? 'late' : (studentData.present ? 'present' : null))) : null;
                const excuse = studentData?.excuse;
                const td = document.createElement('td');
                if (status) {
                        if ((status === 'absent' || status === 'late') && excuse) {
                        td.innerHTML = `<div class="status-indicator ${status}"><div class="excuse-dot"></div></div>`;
                    } else {
                        td.innerHTML = `<div class="status-indicator ${status}"></div>`;
                    }
                }
                studentRow.appendChild(td);
            }
            monthlyTableBody.appendChild(studentRow);
        });
    };
    const populateStudentListForDay = (date) => {
        const studentListContainer = dailyView.querySelector('.student-list');
        studentListContainer.innerHTML = `<div class="list-header"><span class="student-name-header-daily">Nombre del Estudiante</span><span class="attendance-status-header">Estado de Asistencia</span></div>`;
        const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        students.forEach(student => {
            const studentData = attendanceData[dateKey]?.[student.id];
            const isPresent = studentData?.present || false;
            const isAbsent = studentData?.absent || false;
            const isLate = studentData?.late || false;
            const hasExcuse = studentData?.excuse || false;
            const row = document.createElement('div');
            row.className = 'student-row';
            row.dataset.studentId = student.id;
            row.innerHTML = `<div class="student-info"><div class="avatar-small">${student.id}</div><span>${student.name}</span></div><div class="attendance-controls"><button class="status-btn present ${isPresent ? 'selected' : ''}">Presente</button><button class="status-btn absent ${isAbsent ? 'selected' : ''}">Ausente</button><button class="status-btn late ${isLate ? 'selected' : ''}">Tarde</button><div class="excuse-container" style="display: ${isAbsent || isLate ? 'flex' : 'none'};"><label class="excuse-label"><input type="checkbox" class="excuse-checkbox" ${hasExcuse ? 'checked' : ''}> Trajo Excusa</label></div></div>`;
            studentListContainer.appendChild(row);
        });
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
            const absentBtn = row.querySelector('.status-btn.absent');
            const lateBtn = row.querySelector('.status-btn.late');
            const excuseContainer = row.querySelector('.excuse-container');
            const excuseCheckbox = row.querySelector('.excuse-checkbox');
            if (absentBtn.classList.contains('selected') || lateBtn.classList.contains('selected')) {
                excuseContainer.style.display = 'flex';
            } else {
                excuseContainer.style.display = 'none';
                excuseCheckbox.checked = false;
            }
        };
        studentRows.forEach(row => {
            const presentBtn = row.querySelector('.status-btn.present');
            const absentBtn = row.querySelector('.status-btn.absent');
            const lateBtn = row.querySelector('.status-btn.late');
            presentBtn.addEventListener('click', () => {
                presentBtn.classList.toggle('selected');
                if (presentBtn.classList.contains('selected')) {
                    absentBtn.classList.remove('selected');
                } else {
                    lateBtn.classList.remove('selected');
                }
                updateExcuseVisibility(row);
                updateSummary();
            });
            absentBtn.addEventListener('click', () => {
                absentBtn.classList.toggle('selected');
                if (absentBtn.classList.contains('selected')) {
                    presentBtn.classList.remove('selected');
                    lateBtn.classList.remove('selected');
                }
                updateExcuseVisibility(row);
                updateSummary();
            });
            lateBtn.addEventListener('click', () => {
                lateBtn.classList.toggle('selected');
                if (lateBtn.classList.contains('selected')) {
                    presentBtn.classList.add('selected');
                    absentBtn.classList.remove('selected');
                }
                updateExcuseVisibility(row);
                updateSummary();
            });
        });
        updateSummary();
    };
    const saveDailyAttendance = () => {
        const date = selectedDateForDailyView;
        const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        if (!attendanceData[dateKey]) {
            attendanceData[dateKey] = {};
        }
        const studentRows = dailyView.querySelectorAll('.student-row');
        studentRows.forEach(row => {
            const studentId = row.dataset.studentId;
            const presentBtn = row.querySelector('.status-btn.present');
            const absentBtn = row.querySelector('.status-btn.absent');
            const lateBtn = row.querySelector('.status-btn.late');
            const excuseCheckbox = row.querySelector('.excuse-checkbox');
            if (presentBtn.classList.contains('selected') || absentBtn.classList.contains('selected')) {
                attendanceData[dateKey][studentId] = {
                    present: presentBtn.classList.contains('selected'),
                    absent: absentBtn.classList.contains('selected'),
                    late: lateBtn.classList.contains('selected'),
                    excuse: excuseCheckbox.checked
                };
            } else {
                if(attendanceData[dateKey]?.[studentId]) {
                    delete attendanceData[dateKey][studentId];
                }
            }
        });
        showAlert('Asistencia guardada!');
        showMonthlyView();
    };
    prevMonthBtn.addEventListener('click', () => {
        currentDisplayDate.setMonth(currentDisplayDate.getMonth() - 1);
        renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth());
    });
    nextMonthBtn.addEventListener('click', () => {
        currentDisplayDate.setMonth(currentDisplayDate.getMonth() + 1);
        renderMonthlyList(currentDisplayDate.getFullYear(), currentDisplayDate.getMonth());
    });
    goToTodayBtn.addEventListener('click', () => showDailyView(new Date()));
    backToMonthlyBtn.addEventListener('click', showMonthlyView);
    document.getElementById('save-daily-attendance-btn').addEventListener('click', saveDailyAttendance);

    // --- GRADES LOGIC ---
    const gradesTable = document.querySelector('.grades-table');
    const gradesTableHead = gradesTable.querySelector('thead');
    const gradesTableBody = gradesTable.querySelector('tbody');
    const lowestGradeEl = document.getElementById('lowest-grade');
    const highestGradeEl = document.getElementById('highest-grade');
    const averageGradeEl = document.getElementById('average-grade');
    const passingGradeInput = document.getElementById('passing-grade');
    const minGradeInput = document.getElementById('min-grade');
    const maxGradeInput = document.getElementById('max-grade');

    const saveGradesData = () => {
        localStorage.setItem('schoolGrades_students', JSON.stringify(students));
        localStorage.setItem('schoolGrades_assignments', JSON.stringify(assignmentNames));
    };

    const loadGradesData = () => {
        const savedStudents = localStorage.getItem('schoolGrades_students');
        const savedAssignments = localStorage.getItem('schoolGrades_assignments');
        if (savedStudents) {
            students = JSON.parse(savedStudents);
        }
        if (savedAssignments) {
            assignmentNames = JSON.parse(savedAssignments);
        }
    };

    const calculateAllAverages = () => {
        let allGrades = [];
        const passingGrade = parseFloat(passingGradeInput.value) || 60;
        gradesTableBody.querySelectorAll('tr').forEach((row, studentIndex) => {
            let sum = 0;
            let count = 0;
            const inputs = row.querySelectorAll('.grade-input');
            inputs.forEach((input, gradeIndex) => {
                const value = parseFloat(input.value);
                if (!isNaN(value)) {
                    sum += value;
                    count++;
                    allGrades.push(value);
                }
                // Update data model
                students[studentIndex].grades[gradeIndex] = isNaN(value) ? '' : value;
            });
            const average = count > 0 ? (sum / count).toFixed(1) : 'N/A';
            const averageCell = row.querySelector('.average-cell');
            averageCell.textContent = average;
            
            row.classList.remove('failing-student');
            averageCell.classList.remove('failing');

            if (average !== 'N/A' && parseFloat(average) < passingGrade) {
                averageCell.classList.add('failing');
                row.classList.add('failing-student');
            }
        });

        if (allGrades.length > 0) {
            lowestGradeEl.textContent = Math.min(...allGrades).toFixed(1);
            highestGradeEl.textContent = Math.max(...allGrades).toFixed(1);
            const totalAverage = (allGrades.reduce((a, b) => a + b, 0) / allGrades.length).toFixed(1);
            averageGradeEl.textContent = totalAverage;
        } else {
            lowestGradeEl.textContent = '0';
            highestGradeEl.textContent = '0';
            averageGradeEl.textContent = '0';
        }
        saveGradesData();
    };

    const renderGradesTable = () => {
        // Render Header
        gradesTableHead.innerHTML = '';
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `<th class="student-name-header">Nombre</th>`;
        assignmentNames.forEach(name => {
            const th = document.createElement('th');
            th.innerHTML = `<span>${name}</span> <span class="assignment-actions"><i class="fas fa-pencil-alt" data-action="edit-assignment"></i><i class="fas fa-trash-alt delete-assignment-icon" data-action="delete-assignment"></i></span>`;
            headerRow.appendChild(th);
        });
        headerRow.innerHTML += `<th>Promedio</th>`;
        gradesTableHead.appendChild(headerRow);

        // Render Body
        gradesTableBody.innerHTML = '';
        students.forEach(student => {
            const row = document.createElement('tr');
            row.dataset.studentId = student.id;
            let gradeInputs = '';
            student.grades.forEach(grade => {
                gradeInputs += `<td><input type="number" class="grade-input" value="${grade}"></td>`;
            });
            row.innerHTML = `
                <td class="student-name-cell">${student.name}</td>
                ${gradeInputs}
                <td class="average-cell">0</td>
            `;
            gradesTableBody.appendChild(row);
        });
        
        gradesTableBody.querySelectorAll('.grade-input').forEach(input => {
            input.addEventListener('change', (e) => {
                const min = parseFloat(minGradeInput.value);
                const max = parseFloat(maxGradeInput.value);
                let value = parseFloat(e.target.value);

                if (e.target.value !== '' && (value < min || value > max)) {
                    e.target.value = '';
                }
                calculateAllAverages();
            });
        });

        calculateAllAverages();
    };
    
    const updateGradeInputLimits = () => {
        const min = minGradeInput.value;
        const max = maxGradeInput.value;
        gradesTableBody.querySelectorAll('.grade-input').forEach(input => {
                if (input.value !== '' && (parseFloat(input.value) < min || parseFloat(input.value) > max)) {
                input.value = '';
            }
        });
        calculateAllAverages();
    };

    // Grades Actions
    document.getElementById('add-assignment-btn').addEventListener('click', () => {
        showPrompt("Nueva Asignación", "Introduce el nombre de la nueva asignación:", (name) => {
            if (name && name.trim() !== '') {
                assignmentNames.push(name.trim());
                students.forEach(student => {
                    student.grades.push('');
                });
                renderGradesTable();
                saveGradesData();
            }
        });
    });

    document.getElementById('export-grades-btn').addEventListener('click', () => {
        let csvContent = "data:text/csv;charset=utf-8,";
        const headers = ['Nombre', ...assignmentNames, 'Promedio'].map(h => `"${h}"`);
        csvContent += headers.join(',') + '\r\n';

        gradesTableBody.querySelectorAll('tr').forEach(row => {
            const rowData = [];
            rowData.push(`"${row.querySelector('.student-name-cell').textContent}"`);
            row.querySelectorAll('.grade-input').forEach(input => {
                rowData.push(input.value);
            });
            rowData.push(row.querySelector('.average-cell').textContent);
            csvContent += rowData.join(',') + '\r\n';
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "calificaciones.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    document.getElementById('generate-report-btn').addEventListener('click', () => {
        let report = "Reporte de Promedios:\n\n";
        gradesTableBody.querySelectorAll('tr').forEach(row => {
            const name = row.querySelector('.student-name-cell').textContent;
            const average = row.querySelector('.average-cell').textContent;
            report += `${name}: ${average}\n`;
        });
        report += `\nPromedio de la Clase: ${averageGradeEl.textContent}`;
        showAlert(report);
    });

    gradesTableHead.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        if (!action) return;

        const headerCell = e.target.closest('th');
        const columnIndex = Array.from(headerCell.parentNode.children).indexOf(headerCell) - 1;
        const currentName = headerCell.querySelector('span').textContent;

        if (action === 'delete-assignment') {
            showConfirm(`¿Estás seguro de que quieres eliminar la columna "${currentName}"?`, (confirmed) => {
                if (confirmed) {
                    assignmentNames.splice(columnIndex, 1);
                    students.forEach(student => {
                        student.grades.splice(columnIndex, 1);
                    });
                    renderGradesTable();
                    saveGradesData();
                }
            });
        }
        if (action === 'edit-assignment') {
            showPrompt('Editar Asignación', `Introduce el nuevo nombre para "${currentName}":`, (newName) => {
                if (newName && newName.trim() !== '') {
                    assignmentNames[columnIndex] = newName.trim();
                    renderGradesTable();
                    saveGradesData();
                }
            });
        }
    });

    document.querySelectorAll('.grades-settings input').forEach(input => {
        input.addEventListener('change', () => {
            updateGradeInputLimits();
            calculateAllAverages();
        });
    });

    // --- INITIAL RENDER ---
    loadGradesData();
    showMonthlyView();
    renderGradesTable();
});
