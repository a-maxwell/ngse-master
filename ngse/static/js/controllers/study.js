app.controller('studyController', function($rootScope, $scope, $routeParams, $location, formService, authService) {

    $scope.data = {
        "Master of Science": ["CE", "ChE", "CS", "EE", "EgyE", "EnE", "GmE", "IE", "ME", "MetE", "MSE"],
        "Doctor of Philosophy": ["CE", "ChE", "EEE", "EnE", "EgyE", "MSE"],
        "Master of Engineering": ["EE", "IE"],
        "Doctor of Engineering": ["ChE", "EEE", "EgyE"]
    };

    $scope.fields = {
        "CE": ["Geotechnical", "Structural", "Transportation", "Water Resources"],
        "ChE": ["Biological Engineering", "Environmental Engineering", "Fuel Energy & Thermal Systems", "Materials & Catalyst", "Process Systems Engineering"],
        "CS": ["Algorithms & Complexity", "Computer Security", "Computer Vision & Machine Intelligence", "Network & Distributed Systems", "Scientific Computing", "Software Engineering & Service Sciences", "Web Science"],
        "EE": ["Computers & Communications", "Instrumentation & Control", "Microelectronics", "Power Systems"],
        "EgyE": ["Renewable Energy", "Energy Storage", "Biofuels", "Resource Assessment", "Energy Planning", "Energy Modeling", "Waste-to-Energy", "Others:"],
        "EnE": ["Air Quality Management", "Environmental Management", "Geoenvironmental Engineering", "Solid & Hazardous Waste Management", "Water Quality Management"],
        "GmE": ["Applied Geodesy", "Geoinformatics", "Remote Sensing & Photogrammetry"],
        "IE": ["Production Systems", "Human Factors & Ergonomics", "Operations Research", "Information Systems"],
        "ME": ["Automation, Control & Robotics", "Biomechanics", "Computational Mechanics", "Fluids Engineering", "Heating, Ventilation, Air Conditioning & Refrigeration", "Machine Design", "Power", "Vehicle Engineering"],
        "MetE": ["Minerals Processing", "Metal Extraction", "Physical Metallurgy", "Ultrafine Processing"],
        "MSE": ["Metals and Alloys", "Ceramic Materials", "Polymeric Materials", "Composite Materials", "Semiconductor Materials", "Biomaterials", "Nanomaterials", "Materials for Energy", "Green & Environmental Materials", "High-Value Adding of Local Materials", "Materials Forensics (e.g. Corrosion Engineering and Failure Analysis)"],
    }

    $scope.years = ["2017-2018", "2018-2019", "2019-2020", "2020-2021"];

    $scope.levels = Object.keys($scope.data);
    $scope.programs = $scope.data["Master of Science"];

    $scope.level = $scope.levels[0];
    $scope.program = $scope.data[$scope.level][0];
    $scope.option = "thesis";
    $scope.time = "full";
    // $scope.c1 = "";
    // $scope.c2 = "";
    // $scope.c3 = "";
    // $scope.adviser = "";
    $scope.start = "first";
    // $scope.year = "";
    $scope.scholarship = "no";
    // $scope.scholarship_name = "";
    $scope.availableProgram = availableProgram;
    $scope.nonThesisOption = nonThesisOption;
    $scope.thesisOption = thesisOption;
    $scope.otherScholarship = otherScholarship;
    $scope.filter_c2 = filter_c2;
    $scope.filter_c3 = filter_c3;
    $scope.check_c2 = check_c2;
    $scope.check_c3 = check_c3;
    $scope.debug = debug;

    $scope.always = true;

    function debug() {
        console.log($scope.level);
        console.log($scope.program);
        console.log($scope.option);
        console.log($scope.time);
        console.log($scope.c1);
        console.log($scope.c2);
        console.log($scope.c3);
        console.log($scope.adviser);
        console.log($scope.start);
        console.log($scope.year);
        console.log($scope.scholarship);
        console.log($scope.scholarship_name);
    }

    function check_c3() {
        return ($scope.c1 === "" && $scope.c2 === "");
    }

    function check_c2() {
        return ($scope.c1 === "");
    }

    function filter_c3() {
        var labs = [];
        for (var i = 0; i < $scope.fields[$scope.program].length; i++) {
            if ($scope.fields[$scope.program][i] != $scope.c1 && $scope.fields[$scope.program][i] != $scope.c2) {
                labs.push($scope.fields[$scope.program][i]);
            } 
        }
        return labs;
    }

    function filter_c2() {
        var labs = [];
        for (var i = 0; i < $scope.fields[$scope.program].length; i++) {
            if ($scope.fields[$scope.program][i] != $scope.c1) {
                labs.push($scope.fields[$scope.program][i]);
            } 
        }
        return labs;
    }

    function otherScholarship() {
        return ($scope.scholarship === "yes");
    }

    function thesisOption() {
        return ($scope.option === "thesis");
    }

    function nonThesisOption() {
        var programs = ["CE", "ChE", "MSE"]
        if ($scope.level != "Master of Science") {
            $scope.option = "thesis";
            return false;
        }
        for (var i = 0; i < programs.length; i++) if ($scope.program === programs[i]) return true;
        $scope.option = "thesis";
        return false;
    }

    function availableProgram(p) {
        var change = true;
        for (var i = 0; i < $scope.data[$scope.level].length; i++) if ($scope.data[$scope.level][i] === p) return true;
        for (var i = 0; i < $scope.data[$scope.level].length; i++) if ($scope.data[$scope.level][i] === $scope.program) change = false;
        if (change) $scope.program = $scope.data[$scope.level][0];
        return false;
    }

    initController();

    function initController() {
    };
});