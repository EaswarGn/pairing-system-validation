import Link from "next/link";
export default function Navbar() {
    return (
        <div className=" absolute navbar bg-base-100">
            <div className="flex-1">
                <Link href="/" className="btn btn-ghost text-xl">US Chess</Link>
            </div>
            <div className="flex-none">
                <ul className="menu menu-horizontal px-1">
                    <li><Link href="pairing-checker">Pairing Checker</Link></li>
                    <li><Link href="software-validation">Software Validation</Link></li>

                </ul>
            </div>
        </div>
    )
}