import Image from "next/image";
import Link from "next/link";
export default function Home() {
  return (
    <div className="w-screen h-screen flex flex-row items-center justify-center text-white text-4xl" >
      <div className=" flex flex-row w-2/5 h-4/5 items-center justify-center ">
        <div className="flex flex-row w-[300px] h-[300px] items-center justify-center bg-blue-400 rounded-xl">
          <div className="text-center">
            <Link href="/pairing-checker" className="text-white">
              Pairing Checker
            </Link>
          </div>
        </div>
      </div>
      <div className="flex flex-row w-2/5 h-4/5 items-center justify-center ">
        <div className="flex flex-row w-[300px] h-[300px] items-center justify-center  bg-blue-400 rounded-xl">
          <div className="text-center">
            <Link href="/software-validation" className="text-white">
              Software Validation
            </Link>
          </div>

        </div>
      </div>
    </div>

  );
}
