/*
 * @Author: zhaoyang.liang
 * @Github: https://github.com/LzyRapx
 * @Date: 2019-12-16 22:26:50
 */
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cstring>
#include <map>
#include <vector>

using namespace std;

typedef long long ll;

int main() {
    ll n, k;
    cin >> n >> k;
    auto calc = [&](ll x) { // 计算 n 范围内以 x 为最高二进制位的数字数量
        ll res = 0, cnt = 0;
        while((x << cnt) <= n) {
            res += min(1LL << cnt, n - (x << cnt) + 1);
            if(x % 2 == 0) {
                res += max(0LL, min(1LL << cnt, n - ((x + 1) << cnt) + 1));
            }
            cnt++;
        }
        return res;
    };
    ll l = 1, r = n;
    ll ans = 0;
    while(l <= r) {
        ll mid = (l + r) >> 1;
        if(calc(mid) >= k) {
            ans = max(ans, mid);
            l = mid + 1;
        }
        else if(mid - 1 >= l && calc(mid - 1) >= k) {
            ans = max(ans, mid - 1);
            l = mid;
        }
        else {
            r = mid - 1;
        }
    }
    cout << ans << endl;
    return 0;
}
//Backup 67028895 using Codeforces API.