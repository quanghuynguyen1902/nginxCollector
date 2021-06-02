function headers(r) {
    var s = ''
    for (var h in r.headersIn) {
    	if (s.length ) {
            s += ',';
        }
        s += "'"+h+"':'"+r.headersIn[h] + "'";
    }
    return s;
}
export default {headers};
