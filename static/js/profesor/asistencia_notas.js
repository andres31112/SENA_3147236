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
        alertModalBody.innerHTML = message.replace(/\n/g, '<br>');
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
            const dateKey = `${year}-${String(month + 1).padStart(2,'0')}-${String(i).padStart(2,'0')}`;
            const studentData = attendanceData[dateKey]?.[studentId];
            if (studentData && studentData.absent && !studentData.excuse) unexcusedCount++;
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
            if (thisDate.setHours(0,0,0,0) === today.setHours(0,0,0,0)) th.classList.add('today');
            th.addEventListener('click', () => showDailyView(thisDate));
            headerRow.appendChild(th);
        }
        monthlyTableHead.appendChild(headerRow);

        students.forEach(student => {
            const studentRow = document.createElement('tr');
            const unexcused = countUnexcusedAbsences(student.id, year, month);
            if (unexcused >= 3) studentRow.classList.add('highlight-absentee');

            studentRow.innerHTML = `<td class="student-name-cell">${student.name}</td>`;
            for (let i = 1; i <= daysInMonth; i++) {
                const dateKey = `${year}-${String(month + 1).padStart(2,'0')}-${String(i).padStart(2,'0')}`;
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
        const dateKey = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
        students.forEach(student => {
            const studentData = attendanceData[dateKey]?.[student.id];
            const isPresent = studentData?.present || false;
            const isAbsent = studentData?.absent || false;
            const isLate = studentData?.late || false;
            const hasExcuse = studentData?.excuse || false;

            const row = document.createElement('div');
            row.className = 'student-row';
            row.dataset.studentId = student.id;
            row.innerHTML = `
                <div class="student-info"><div class="avatar-small">${student.id}</div><span>${student.name}</span></div>
                <div class="attendance-controls">
                    <button class="status-btn present ${isPresent?'selected':''}">Presente</button>
                    <button class="status-btn absent ${isAbsent?'selected':''}">Ausente</button>
                    <button class="status-btn late ${isLate?'selected':''}">Tarde</button>
                    <div class="excuse-container" style="display: ${(isAbsent||isLate)?'flex':'none'};">
                        <label class="excuse-label"><input type="checkbox" class="excuse-checkbox" ${hasExcuse?'checked':''}> Trajo Excusa</label>
                    </div>
                </div>`;
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
                if (presentBtn.classList.contains('selected')) absentBtn.classList.remove('selected'); else lateBtn.classList.remove('selected');
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
        const dateKey = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
        if (!attendanceData[dateKey]) attendanceData[dateKey] = {};
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
                if(attendanceData[dateKey]?.[studentId]) delete attendanceData[dateKey][studentId];
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
    goToTodayBtn.addEventListener('click', () => {
        currentDisplayDate = new Date();
        showDailyView(currentDisplayDate);
    });
    backToMonthlyBtn.addEventListener('click', showMonthlyView);
    document.getElementById('save-daily-attendance-btn').addEventListener('click', saveDailyAttendance);

    showMonthlyView();

    // --- GRADES LOGIC ---
    const gradesTable = document.querySelector('.grades-table');
    const minGradeInput = document.getElementById('min-grade');
    const maxGradeInput = document.getElementById('max-grade');
    const passingGradeInput = document.getElementById('passing-grade');

    const renderGradesTable = () => {
        const thead = gradesTable.querySelector('thead');
        const tbody = gradesTable.querySelector('tbody');
        thead.innerHTML = '';
        tbody.innerHTML = '';
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `<th>Estudiante</th>` + assignmentNames.map(a => `<th>${a}</th>`).join('');
        thead.appendChild(headerRow);

        students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${student.name}</td>` + assignmentNames.map(a => {
                const grade = student.grades[a] ?? '';
                return `<td>${grade}</td>`;
            }).join('');
            tbody.appendChild(row);
        });
    };

    document.getElementById('add-assignment-btn').addEventListener('click', () => {
        showPrompt('Nueva Asignación', 'Ingrese el nombre de la nueva asignación:', value => {
            if(value) {
                assignmentNames.push(value);
                students.forEach(s => s.grades[value] = 0);
                renderGradesTable();
            }
        });
    });

    renderGradesTable();
});
